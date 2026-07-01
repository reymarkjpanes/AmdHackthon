# Clausify AI — Full System Documentation

## 1. Project Overview

**Clausify AI** is an enterprise document intelligence platform built for the **AMD Developer Hackathon: ACT II**. It enables users to upload business documents (contracts, quotations, invoices, images) and receive AI-powered analysis including:

- Executive summaries
- Risk identification and categorization
- Cross-document conflict detection
- Supplier/option comparison matrices
- Actionable recommendations with confidence scores
- Interactive RAG-powered chat copilot with streaming responses
- Exportable AMD-branded PDF reports

The platform is powered by **AMD Instinct MI300X** GPU hardware for accelerated inference and embedding generation.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                    │
│  Landing → Upload → Dashboard → Chat                         │
│  React 18 | TypeScript | Tailwind CSS 4 | React Router 7     │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API + SSE Streaming
┌─────────────────────────▼───────────────────────────────────┐
│                  BACKEND (FastAPI + Python)                   │
│  Routers: upload | analyze | chat | report | demo            │
├──────────────────────────────────────────────────────────────┤
│  Services:                                                    │
│  ┌──────────────┐ ┌────────────────┐ ┌──────────────────┐   │
│  │ LLM Service  │ │ Embedding Svc  │ │ Document Parser  │   │
│  │ (Groq/Claude │ │ (MiniLM-L6-v2) │ │ (PyMuPDF + OCR)  │   │
│  │  /AMD Cloud) │ │ 384-dim vectors│ │                   │   │
│  └──────────────┘ └────────────────┘ └──────────────────┘   │
│  ┌──────────────┐ ┌────────────────┐ ┌──────────────────┐   │
│  │ Vector Store │ │ Session Mgr    │ │ Analysis Service │   │
│  │ (ChromaDB)   │ │ (JSON on disk) │ │ (Orchestrator)   │   │
│  └──────────────┘ └────────────────┘ └──────────────────┘   │
│  ┌──────────────┐ ┌────────────────┐                         │
│  │ Conflict Eng │ │ PDF Generator  │                         │
│  │ (Pairwise)   │ │ (ReportLab)    │                         │
│  └──────────────┘ └────────────────┘                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.11+ | Runtime |
| FastAPI 0.115.5 | Web framework |
| Uvicorn | ASGI server |
| ChromaDB 0.5.23 | Vector database (persistent) |
| sentence-transformers 3.3.1 | Embedding model (all-MiniLM-L6-v2) |
| PyMuPDF 1.24.14 | PDF text extraction |
| pytesseract 0.3.13 | OCR for images/scanned PDFs |
| Pillow 11.0.0 | Image processing |
| Groq SDK 0.13.1 | LLM inference (Llama 3.3 70B) |
| Anthropic SDK 0.40.0 | Claude fallback |
| ReportLab 4.2.5 | PDF report generation |
| python-docx 1.1.2 | DOCX extraction |
| slowapi 0.1.9 | Rate limiting |
| Pydantic 2.10.3 | Data validation |
| python-dotenv 1.0.1 | Environment management |

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18.3.1 | UI framework |
| TypeScript | Type safety |
| Vite 6.3.5 | Build tool |
| Tailwind CSS 4.1.12 | Styling |
| React Router 7.13.0 | Client-side routing |
| Recharts 2.15.2 | Data visualization |
| Lucide React 0.487.0 | Icons |
| Sonner 2.0.3 | Toast notifications |
| Radix UI | Accessible primitives |

---

## 4. Backend — Detailed Architecture

### 4.1 Entry Point (`backend/main.py`)

The FastAPI application initializes all services at startup and injects them into router modules:

```python
# Service initialization order:
1. DocumentParser        → Text extraction from files
2. EmbeddingService      → Load sentence-transformer model + warmup
3. VectorStore           → ChromaDB persistent client
4. SessionManager        → Load persisted sessions from disk
5. LLMService            → Connect to Groq/Claude/AMD
6. ConflictEngine        → Cross-document analysis (uses LLM)
7. AnalysisService       → Full pipeline orchestrator
8. PDFGenerator          → Report generation
```

**Middleware:**
- CORS (configurable origins via `ALLOWED_ORIGINS` env var)
- SlowAPI rate limiting (60 requests/minute default)
- Global exception handler (500 errors never expose stack traces)

**Health Check:** `GET /health` returns `{"status": "ok", "version": "1.0.0"}`

---

### 4.2 Routers (API Endpoints)

#### 4.2.1 Upload Router (`POST /api/upload`)

**Purpose:** Accept multipart file uploads, extract text, generate embeddings, store in vector DB.

**Flow:**
1. Validate file count (1–10) and file size (max 10MB each)
2. Validate MIME types (PDF, PNG, JPEG, DOCX) — with extension-based inference fallback
3. For each file:
   - Extract text via `DocumentParser`
   - Chunk text via `EmbeddingService.chunk_text()` (512 tokens, 50 token overlap)
   - Generate 384-dim embeddings via `EmbeddingService.embed_batch()`
   - Build `Chunk` objects with metadata
4. Store all chunks in ChromaDB via `VectorStore.add_chunks()`
5. Create session via `SessionManager.create_session()`
6. Return `UploadResponse` with session ID and per-document status

**Response:**
```json
{
  "sessionId": "uuid",
  "documents": [
    {
      "id": "uuid",
      "filename": "contract.pdf",
      "fileType": "pdf",
      "fileSize": 2456789,
      "uploadedAt": "2026-01-15T10:00:00.000Z",
      "processingStatus": "completed"
    }
  ],
  "message": "Successfully processed 3 of 3 document(s)."
}
```

#### 4.2.2 Session Check (`GET /api/session/{session_id}/check`)

**Purpose:** Lightweight endpoint for frontend to validate stored session on app load.

**Returns:** `200 {"valid": true}` or `404 {"valid": false}`

---

#### 4.2.3 Analyze Router (`POST /api/analyze`)

**Purpose:** Run the full AI analysis pipeline on uploaded documents.

**Rate Limit:** 5 requests/minute per IP

**Flow:**
1. Validate session exists
2. Retrieve all chunks from ChromaDB
3. Run parallel LLM calls via `AnalysisService`:
   - Batch 1: Executive summary + Risk analysis + Suggested questions
   - 0.5s delay (rate limit protection)
   - Batch 2: Comparison matrix + Recommendation + Conflict detection
4. Store results in session
5. Return complete `AnalyzeResponse`

**Response:**
```json
{
  "sessionId": "uuid",
  "status": "completed",
  "analysis": {
    "analyzedAt": "ISO8601",
    "executiveSummary": "...",
    "risks": [...],
    "comparisonMatrix": [...],
    "conflicts": [...],
    "recommendation": {...},
    "suggestedQuestions": [...]
  }
}
```

#### 4.2.4 Suggest Questions (`POST /api/suggest-questions`)

**Purpose:** Generate 6 contextually-relevant quick questions based on document content.

**Rate Limit:** 10 requests/minute per IP

---

#### 4.2.5 Chat Router (`POST /api/chat`)

**Purpose:** RAG-powered Q&A over uploaded documents with structured responses.

**Flow:**
1. Validate session and question
2. Embed the question → 384-dim vector
3. Retrieve top-8 semantically similar chunks from ChromaDB
4. If fewer than 3 chunks retrieved, supplement with all session chunks (up to 12)
5. Build hybrid prompt (document content + conversation history + expert persona)
6. Call LLM with `system_prompt` + `user_prompt`
7. Parse structured JSON response (answer, evidence, risks, recommendation)
8. Return `ChatResponse` with processing time

**Structured Response Format:**
```json
{
  "messageId": "uuid",
  "role": "assistant",
  "structuredResponse": {
    "answer": "Substantive answer grounded in documents + expert context",
    "evidence": [
      {
        "quote": "Verbatim excerpt from document (max 200 chars)",
        "sourceDocument": "filename.pdf",
        "documentType": "pdf"
      }
    ],
    "risks": "Specific risks with severity",
    "recommendation": "Clear next step with owner and timeframe"
  },
  "processingTimeMs": 2340
}
```

#### 4.2.6 Chat Stream (`POST /api/chat/stream`)

**Purpose:** Server-Sent Events streaming variant of the chat endpoint.

**Event Types:**
- `token` — Individual word tokens streamed at ~55 words/sec
- `done` — Final event with complete structured response
- `error` — Error event with message and code

**SSE Format:**
```
data: {"type": "token", "text": "Based "}
data: {"type": "token", "text": "on "}
data: {"type": "token", "text": "the "}
...
data: {"type": "done", "messageId": "...", "structuredResponse": {...}, "processingTimeMs": 2340}
```

#### 4.2.7 Report Router (`POST /api/report`)

**Purpose:** Generate and download an AMD-branded PDF report.

**Returns:** Binary PDF with `Content-Type: application/pdf`

**PDF Contents:**
- Title page (AMD branding, report metadata)
- Executive summary
- Risk analysis table (color-coded by severity)
- Supplier comparison matrix
- Detected conflicts with side-by-side excerpts
- Final recommendation with confidence score
- Footer with AMD MI300X branding

#### 4.2.8 Demo Router (`GET /api/demo`)

**Purpose:** Return pre-loaded static demo data without requiring file upload.

**Demo Scenario:** 5 procurement documents (2 supplier quotations, 1 existing contract, 1 invoice, 1 procurement policy) with pre-computed analysis and 2 pre-seeded chat Q&A pairs.

---

### 4.3 Services — Detailed

#### 4.3.1 LLM Service (`services/llm_service.py`)

**Multi-provider abstraction supporting:**

| Provider | Model | Selection |
|----------|-------|-----------|
| GROQ (default) | Llama 3.3 70B Versatile | `LLM_PROVIDER=GROQ` |
| CLAUDE | Claude 3.5 Sonnet | `LLM_PROVIDER=CLAUDE` |
| AMD | Llama 3.2 Vision 11B | `LLM_PROVIDER=AMD` |

**Key Methods:**
- `complete(system_prompt, user_prompt, max_tokens)` → Raw string response
- `_parse_with_retry(system_prompt, user_prompt, model_class)` → Pydantic model with retry on parse failure

**Error Handling:**
- `LLMRateLimitError` — Rate limit detection (429, quota exceeded)
- `LLMParseError` — Invalid JSON from LLM
- `ConfigurationError` — Missing API keys

**Helper:** `_strip_json_fences(text)` — Removes markdown code fences and control characters from LLM output.

---

#### 4.3.2 Embedding Service (`services/embedding_service.py`)

**Model:** `all-MiniLM-L6-v2` (384-dimensional vectors)

**Methods:**
- `embed(text)` → Single 384-dim normalized vector
- `embed_batch(texts)` → Batch processing (batch_size=32) for efficiency
- `chunk_text(text, max_tokens=512, overlap=50)` → Word-based text splitting with configurable overlap

**Chunking Strategy:**
- Uses word-based approximation: 1 token ≈ 0.75 words
- Default chunk size: ~384 words (512 tokens × 0.75)
- Overlap: ~37 words between consecutive chunks
- Single documents shorter than one chunk are returned as-is

**AMD Optimization:** Designed for ROCm GPU acceleration on MI300X hardware (auto-detected).

---

#### 4.3.3 Vector Store (`services/vector_store.py`)

**Backend:** ChromaDB PersistentClient

**Storage:** `backend/data/chroma/` directory (configurable via `CHROMA_PERSIST_DIR`)

**Session Isolation:** Each session gets its own ChromaDB collection named `session_{uuid_with_underscores}`

**Methods:**
- `add_chunks(session_id, chunks)` → Store chunks with embeddings and metadata
- `query_top_k(session_id, embedding, k=5)` → Semantic similarity search
- `get_all_chunks(session_id)` → Retrieve all chunks for a session
- `collection_exists(session_id)` → Check if collection has data

**Metadata stored per chunk:**
- `source_document` — Original filename
- `document_type` — "pdf" or "image"
- `chunk_index` — Position within the source document

---

#### 4.3.4 Session Manager (`services/session_manager.py`)

**Persistence:** JSON files on disk at `backend/data/sessions/{session_id}.json`

**Survives restarts:** Sessions are loaded from disk on service initialization.

**Data Model:**
```python
@dataclass
class SessionData:
    session_id: str
    documents: list[UploadedDocument]
    analysis: Optional[AnalysisResult]
    created_at: datetime
```

**Methods:**
- `create_session(session_id, documents)` → Create + persist
- `get_session(session_id)` → Retrieve (raises `SessionNotFoundError` if missing)
- `store_analysis(session_id, analysis)` → Attach analysis results + persist
- `session_exists(session_id)` → Boolean check

---

#### 4.3.5 Document Parser (`services/document_parser.py`)

**Supported formats:**
| Format | Method | Fallback |
|--------|--------|----------|
| PDF | PyMuPDF text extraction | OCR via pytesseract for image-only pages |
| PNG/JPEG | pytesseract OCR | Image metadata description |
| DOCX | python-docx paragraph extraction | — |

**PDF Processing:**
1. Open with PyMuPDF (`fitz`)
2. Extract text from each page
3. If page has no extractable text → render at 2× resolution → OCR with pytesseract
4. Concatenate all pages

**Image Processing:**
1. Open with Pillow, convert to RGB if needed
2. Run pytesseract OCR
3. If OCR fails/empty → return metadata fallback (dimensions, file size)

---

#### 4.3.6 Analysis Service (`services/analysis_service.py`)

**Orchestrates the full analysis pipeline in parallel:**

```
Batch 1 (parallel):     Batch 2 (parallel, after 0.5s delay):
├── Executive Summary    ├── Comparison Matrix
├── Risk Analysis        ├── Recommendation
└── Suggested Questions  └── Conflict Detection
```

**Sub-methods:**
- `_generate_summary()` → Calls LLM with summary prompt, parses JSON
- `_generate_risks()` → Calls LLM with risk prompt, returns `list[Risk]`
- `_generate_comparison_matrix()` → Calls LLM, robust JSON extraction with multiple parse attempts
- `_generate_recommendation()` → Calls LLM, returns `Recommendation` with fallback
- `_generate_suggested_questions()` → Generates 6 short contextual questions

**Error Handling:** Each sub-task handles its own exceptions — non-critical failures (matrix, conflicts, questions) use empty defaults; critical failures (summary, risks, recommendation) raise to caller.

---

#### 4.3.7 Conflict Engine (`services/conflict_engine.py`)

**Algorithm:**
1. Group chunks by source document
2. Generate all pairwise combinations of documents
3. For each pair: send both documents' content to LLM with conflict detection prompt
4. Parse returned conflicts, assign unique IDs
5. Return aggregated conflict list

**Detection focuses on:**
- Price/value discrepancies
- Conflicting dates or deadlines
- Contradictory terms or conditions
- Mismatched quantities or specifications
- Incompatible obligations

**Severity Levels:**
- HIGH — Direct financial impact or legal liability
- MEDIUM — Significant operational inconsistency
- LOW — Minor discrepancy worth flagging

---
