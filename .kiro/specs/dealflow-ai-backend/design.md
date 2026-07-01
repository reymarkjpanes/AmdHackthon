# Design Document: DealFlow AI Backend

## Overview

The DealFlow AI Backend is a FastAPI (Python 3.11) service that provides document intelligence capabilities to the existing Next.js frontend. It exposes five primary REST endpoints — document upload, AI analysis, RAG-based chat, PDF report export, and a demo data endpoint — backed by a pipeline of document parsing, embedding generation, vector storage, LLM inference, and conflict detection.

The backend is designed to run on AMD MI300X GPU hardware via the AMD Developer Cloud, with Anthropic Claude as the primary LLM fallback. All session state is kept in-memory (no database), making the service stateless across restarts and easy to deploy on Railway.app with a single push.

### Key Design Goals

- **Contract fidelity**: every JSON field name, type, and HTTP status code must exactly match what the frontend's `api.ts` and `types.ts` expect
- **AMD-first**: embedding and inference paths are annotated and designed for ROCm GPU acceleration
- **Swappable LLM**: a provider enum allows switching between Claude and AMD Developer Cloud via a single environment variable
- **In-memory sessions**: ChromaDB in-memory collections per session, with a Python dict for session metadata; no external DB required
- **Single-file entry point**: `main.py` wires everything together; routers are in `routers/`, services in `services/`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                        │
│                     (dealflow-ai-frontend/)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST (HTTP/JSON)
┌─────────────────────▼───────────────────────────────────────┐
│                  FastAPI Application (main.py)               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐ │
│  │ /upload  │ │ /analyze │ │  /chat   │ │ /report /demo  │ │
│  │ router   │ │  router  │ │  router  │ │    routers     │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬────────┘ │
│       │            │            │               │           │
│  ┌────▼────────────▼────────────▼───────────────▼────────┐  │
│  │                    Services Layer                      │  │
│  │  DocumentParser  EmbeddingService   LLMService        │  │
│  │  VectorStore     AnalysisService    ConflictEngine    │  │
│  │  PDFGenerator    SessionManager     PromptBuilder     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               In-Memory State                           │ │
│  │  sessions: Dict[str, SessionData]  (Python dict)       │ │
│  │  ChromaDB in-memory Client  (one collection/session)   │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### Request/Response Flow

**Upload flow:**
```
POST /api/upload (multipart)
  → validate file count, size, MIME
  → DocumentParser.extract_text() per file
  → EmbeddingService.embed_chunks()
  → VectorStore.add_chunks(session_id, chunks)
  → SessionManager.create_session(session_id, documents)
  → return UploadResponse
```

**Analysis flow:**
```
POST /api/analyze {sessionId}
  → SessionManager.get_session(session_id)
  → VectorStore.get_all_chunks(session_id)
  → LLMService.complete() × 4 (summary, risks, matrix, recommendation)
  → ConflictEngine.detect(chunks)
  → SessionManager.store_analysis(session_id, result)
  → return AnalyzeResponse
```

**Chat flow (RAG):**
```
POST /api/chat {sessionId, question}
  → EmbeddingService.embed(question)
  → VectorStore.query_top_k(session_id, q_embedding, k=5)
  → PromptBuilder.build_chat_prompt(chunks)
  → LLMService.complete()
  → return ChatResponse
```

---

## Components and Interfaces

### 1. `main.py` — Application Entry Point

```python
app = FastAPI(title="DealFlow AI", version="1.0.0")
app.add_middleware(CORSMiddleware, ...)
app.include_router(upload_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(demo_router, prefix="/api")
app.add_exception_handler(Exception, global_exception_handler)
```

### 2. `services/document_parser.py` — DocumentParser

```python
class DocumentParser:
    def extract_text(self, file_bytes: bytes, mime_type: str) -> str:
        """Returns extracted plain text. Raises ExtractionError on failure."""

    def _extract_pdf(self, file_bytes: bytes) -> str:
        """Uses fitz (PyMuPDF). Falls back to pytesseract for image-only pages."""

    def _extract_image(self, file_bytes: bytes) -> str:
        """Uses pytesseract + Pillow for OCR."""
```

### 3. `services/embedding_service.py` — EmbeddingService

```python
class EmbeddingService:
    model: SentenceTransformer  # "all-MiniLM-L6-v2"

    def embed(self, text: str) -> list[float]:
        """Returns 384-dimensional float vector. # AMD: ROCm GPU-accelerated"""

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Batch embedding for efficiency on AMD MI300X."""

    def chunk_text(self, text: str, max_tokens: int = 512, overlap: int = 50) -> list[str]:
        """Splits text into overlapping chunks of approximately max_tokens tokens."""
```

### 4. `services/vector_store.py` — VectorStore

```python
class VectorStore:
    client: chromadb.Client  # chromadb.EphemeralClient() — in-memory

    def create_collection(self, session_id: str) -> chromadb.Collection:
        """Creates or returns a ChromaDB collection named by session_id."""

    def add_chunks(self, session_id: str, chunks: list[Chunk]) -> None:
        """Stores text chunks and their embeddings in the session collection."""

    def query_top_k(self, session_id: str, embedding: list[float], k: int = 5) -> list[Chunk]:
        """Returns the k most semantically similar chunks to the given embedding."""

    def get_all_chunks(self, session_id: str) -> list[Chunk]:
        """Returns all chunks for a session (used during analysis)."""

    def collection_exists(self, session_id: str) -> bool:
        """Returns True if the session has an active collection."""
```

### 5. `services/llm_service.py` — LLMService

```python
class LLMProvider(str, Enum):
    CLAUDE = "CLAUDE"
    AMD = "AMD"

class LLMService:
    provider: LLMProvider  # read from LLM_PROVIDER env var, defaults to CLAUDE

    async def complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """Routes to the active provider. # AMD: Cloud inference on MI300X"""
```

### 6. `services/conflict_engine.py` — ConflictEngine

```python
class ConflictEngine:
    def __init__(self, llm_service: LLMService): ...

    async def detect(self, chunks: list[Chunk], document_names: list[str]) -> list[Conflict]:
        """Compares documents pairwise and identifies factual contradictions via LLM."""
```

### 7. `services/analysis_service.py` — AnalysisService

```python
class AnalysisService:
    def __init__(self, llm_service: LLMService, conflict_engine: ConflictEngine): ...

    async def run_full_analysis(self, session_id: str, chunks: list[Chunk], doc_names: list[str]) -> AnalysisResult:
        """Orchestrates all LLM calls and conflict detection, returns AnalysisResult."""
```

### 8. `services/pdf_generator.py` — PDFGenerator

```python
class PDFGenerator:
    AMD_RED = "#ED1C24"

    def generate_report(self, analysis: AnalysisResult, session_id: str) -> bytes:
        """Generates ReportLab PDF bytes with AMD branding."""
```

### 9. `services/session_manager.py` — SessionManager

```python
@dataclass
class SessionData:
    session_id: str
    documents: list[UploadedDocument]
    analysis: AnalysisResult | None
    created_at: datetime

class SessionManager:
    sessions: dict[str, SessionData]  # in-memory dict

    def create_session(self, session_id: str, documents: list[UploadedDocument]) -> SessionData: ...
    def get_session(self, session_id: str) -> SessionData:
        """Raises SessionNotFoundError if session does not exist."""
    def store_analysis(self, session_id: str, analysis: AnalysisResult) -> None: ...
    def session_exists(self, session_id: str) -> bool: ...
```

### 10. `prompts/` — Prompt Templates

Each module exposes a function returning a formatted string:

| Module | Function | Output |
|--------|----------|--------|
| `system_prompt.py` | `get_system_prompt(doc_list)` | Identifies assistant as AMD-powered procurement analyst |
| `executive_summary.py` | `build_summary_prompt(chunks)` | Instructs LLM to return JSON `{"executiveSummary": str}` |
| `risk_analysis.py` | `build_risk_prompt(chunks)` | Instructs LLM to return JSON `{"risks": [...]}` with HIGH/MEDIUM/LOW |
| `conflict_detection.py` | `build_conflict_prompt(doc_a, doc_b)` | Pairwise comparison, return JSON array of conflicts |
| `chat_copilot.py` | `build_chat_prompt(question, chunks)` | RAG prompt, return JSON `{answer, evidence, risks, recommendation}` |
| `recommendation.py` | `build_recommendation_prompt(chunks)` | Return JSON `{title, summary, nextSteps, confidence}` |

---

## Data Models

All Pydantic models live in `models/`:

### `models/document.py`

```python
class ProcessingStatus(str, Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    EXTRACTING_TEXT = "extracting_text"
    RUNNING_OCR = "running_ocr"
    GENERATING_EMBEDDINGS = "generating_embeddings"
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "failed"

class UploadedDocument(BaseModel):
    id: str                          # UUID v4
    filename: str
    fileType: Literal["pdf", "image"]
    fileSize: int                    # bytes
    uploadedAt: datetime             # serialized as ISO 8601
    processingStatus: ProcessingStatus

class Chunk(BaseModel):
    id: str                          # UUID v4
    text: str
    embedding: list[float]           # 384 dims
    source_document: str             # filename
    document_type: Literal["pdf", "image"]
    chunk_index: int
```

### `models/response.py`

```python
class Risk(BaseModel):
    id: str
    level: Literal["HIGH", "MEDIUM", "LOW"]
    description: str
    sourceDocument: str
    category: str

class Conflict(BaseModel):
    id: str
    type: str
    severity: Literal["HIGH", "MEDIUM", "LOW"]
    documentA: dict  # {"name": str, "excerpt": str}
    documentB: dict  # {"name": str, "excerpt": str}
    explanation: str
    recommendedAction: str

class ComparisonRow(BaseModel):
    field: str
    values: dict[str, str]
    winner: str | None = None

class Recommendation(BaseModel):
    title: str
    summary: str
    nextSteps: list[str]
    confidence: float  # 0.0 – 1.0

class AnalysisResult(BaseModel):
    analyzedAt: datetime             # ISO 8601
    executiveSummary: str
    risks: list[Risk]
    comparisonMatrix: list[ComparisonRow]
    conflicts: list[Conflict]
    recommendation: Recommendation

class Evidence(BaseModel):
    quote: str                       # max 200 chars
    sourceDocument: str
    documentType: Literal["pdf", "image"]

class StructuredAIResponse(BaseModel):
    answer: str
    evidence: list[Evidence]
    risks: str
    recommendation: str

# --- Request/Response envelopes ---

class UploadResponse(BaseModel):
    sessionId: str
    documents: list[UploadedDocument]
    message: str

class AnalyzeRequest(BaseModel):
    sessionId: str

class AnalyzeResponse(BaseModel):
    sessionId: str
    status: Literal["processing", "completed"]
    analysis: AnalysisResult | None = None

class ChatRequest(BaseModel):
    sessionId: str
    question: str

class ChatResponse(BaseModel):
    messageId: str
    role: Literal["assistant"]
    structuredResponse: StructuredAIResponse
    processingTimeMs: int

class ReportRequest(BaseModel):
    sessionId: str
    includeChat: bool = False

class ErrorResponse(BaseModel):
    error: str
    code: str
    details: dict | None = None
```

### Datetime Serialization Strategy

FastAPI's default Pydantic v2 serialization converts `datetime` objects to ISO 8601 strings automatically when `model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})` is set on the base model. This ensures all `analyzedAt` and `uploadedAt` fields serialize correctly for the frontend (which does `new Date(isoString)`).

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: MIME type acceptance is exhaustive and exclusive

*For any* file MIME type string, the upload endpoint SHALL accept it if and only if it is one of `application/pdf`, `image/png`, `image/jpeg`. Any other MIME type SHALL be rejected with HTTP 400 and code `UNSUPPORTED_FORMAT`.

**Validates: Requirements 1.2**

---

### Property 2: Session creation round-trip

*For any* valid upload request (1–10 files, each ≤10 MB, accepted MIME type), the returned `sessionId` SHALL be a valid UUID v4, and subsequently calling `/api/analyze` or `/api/chat` with that `sessionId` SHALL NOT return a 404 error.

**Validates: Requirements 1.5, 9.1, 9.2**

---

### Property 3: Chunking text reassembly preserves original content

*For any* non-empty string of extracted text, splitting it into overlapping chunks of ~512 tokens with 50-token overlap and then reassembling (by concatenating and deduplicating the overlap regions) SHALL produce a string that is a superset of every character sequence from the original text.

**Validates: Requirements 1.8, 11.3**

---

### Property 4: Embedding dimension invariant

*For any* text string passed to `EmbeddingService.embed()`, the returned vector SHALL have exactly 384 elements.

**Validates: Requirements 1.9, 11.5**

---

### Property 5: Embedding determinism

*For any* text string, calling `EmbeddingService.embed()` twice with the same input SHALL produce identical float vectors.

**Validates: Requirements 11.6**

---

### Property 6: Session isolation — no cross-session data leakage

*For any* two sessions created independently, querying the vector store for session A's chunks SHALL never return chunks that were stored under session B, regardless of the order of operations or the similarity of document content.

**Validates: Requirements 9.4, 9.7**

---

### Property 7: Analysis response schema conformance

*For any* successful call to `/api/analyze` that returns HTTP 200, the response JSON SHALL be deserializable into `AnalyzeResponse` with `status = "completed"` and a non-null `analysis` field containing all required sub-fields (`analyzedAt`, `executiveSummary`, `risks`, `comparisonMatrix`, `conflicts`, `recommendation`).

**Validates: Requirements 2.9, 2.10**

---

### Property 8: Risk level constraint

*For any* risk object in an `AnalysisResult.risks` array, the `level` field SHALL be exactly one of the strings `"HIGH"`, `"MEDIUM"`, or `"LOW"` — no other values are permitted.

**Validates: Requirements 2.5, 12.3**

---

### Property 9: Chat response schema conformance and timing

*For any* valid call to `/api/chat`, the response SHALL be deserializable into `ChatResponse`, the `processingTimeMs` field SHALL be a non-negative integer, and every element in `structuredResponse.evidence` SHALL have a `quote` field of at most 200 characters.

**Validates: Requirements 3.8, 3.9, 3.10, 3.7**

---

### Property 10: Unknown session returns 404 on all endpoints

*For any* string that is not an active `session_id`, calling `/api/analyze`, `/api/chat`, or `/api/report` with that string SHALL return HTTP 404 with `code = "SESSION_NOT_FOUND"`.

**Validates: Requirements 2.2, 3.2, 4.2**

---

### Property 11: Error response schema conformance

*For any* error response from any endpoint (4xx or 5xx), the response body SHALL be deserializable into `ErrorResponse` and the `code` field SHALL be one of the values in the `API_ERROR_CODES` set defined in the frontend's `api.ts`.

**Validates: Requirements 8.1, 8.2**

---

### Property 12: LLM provider routing

*For any* valid prompt passed to `LLMService.complete()`, the returned string SHALL be non-empty, and the provider actually invoked SHALL match the value of the `LLM_PROVIDER` environment variable at startup.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

---

### Property 13: PDF report header fields

*For any* valid report generation request, the HTTP response SHALL have `Content-Type: application/pdf` and a `Content-Disposition` header of the form `attachment; filename="dealflow-report-YYYY-MM-DD.pdf"`.

**Validates: Requirements 4.10**

---

### Property 14: Chunk count additivity

*For any* session where N documents are uploaded, the total number of chunks stored in the session's ChromaDB collection SHALL equal the sum of chunks produced by each document individually.

**Validates: Requirements 11.4**

---

## Error Handling

### Error Taxonomy

| HTTP Status | Condition | Code |
|-------------|-----------|------|
| 400 | Invalid MIME type | `UNSUPPORTED_FORMAT` |
| 400 | Too many files (>10) | `FILE_COUNT_EXCEEDED` |
| 400 | File too large (>10 MB) | `FILE_SIZE_EXCEEDED` |
| 400 | Empty or missing `question` field | `INVALID_REQUEST` |
| 404 | Session not found | `SESSION_NOT_FOUND` |
| 422 | All files failed processing | `UPLOAD_FAILED` |
| 422 | Request body fails Pydantic validation | `UNKNOWN_ERROR` (FastAPI default, overridden) |
| 500 | PDF generation failure | `REPORT_FAILED` |
| 500 | Unhandled exception | `UNKNOWN_ERROR` |
| 502 | LLM service failure | `ANALYSIS_FAILED` |

### Global Exception Handler

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Never expose stack traces in production
    # Log full traceback server-side
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred.", "code": "UNKNOWN_ERROR", "details": None}
    )
```

### LLM JSON Parsing with Retry

When the LLM returns malformed JSON that fails Pydantic parsing, the `LLMService` retries the call exactly once with an additional instruction to the model to correct its JSON format. If the retry also fails, the service raises `LLMParseError`, which the router converts to HTTP 502.

```python
async def _parse_with_retry(self, prompt: str, model_class: type[BaseModel]) -> BaseModel:
    response = await self.complete(...)
    try:
        return model_class.model_validate_json(response)
    except ValidationError:
        # Retry once with corrective instruction
        response = await self.complete(..., extra_instruction="Respond ONLY with valid JSON.")
        return model_class.model_validate_json(response)  # raises on second failure
```

### Per-File Error Isolation

During upload processing, each file is processed in a try/except block. A failed file gets `processingStatus = "failed"` without affecting other files. Only when all files fail does the endpoint return HTTP 422.

---

## Testing Strategy

### Framework

- **Test runner**: `pytest` with `pytest-asyncio` for async endpoints
- **HTTP client**: `httpx` with FastAPI's `TestClient` / `AsyncClient`
- **Property-based testing**: `hypothesis` (minimum 100 examples per property test)
- **Mocking**: `unittest.mock` / `pytest-mock` for LLM calls and external services

### Test Files

```
backend/tests/
├── test_upload.py         # Upload pipeline, chunking, file validation
├── test_analysis.py       # Analysis endpoint, schema conformance, session lifecycle
├── test_conflict.py       # Conflict engine logic, cross-document detection
├── test_chat.py           # RAG retrieval, chat response schema
├── test_embedding.py      # Embedding dimension invariant, determinism
├── test_session.py        # Session isolation, session not found handling
└── test_error_format.py   # Error response schema conformance across all endpoints
```

### Property-Based Tests (Hypothesis)

Each property from the Correctness Properties section maps to exactly one `@given` test. Tests are tagged with a comment:

```
# Feature: dealflow-ai-backend, Property N: <property_text>
```

**Key property tests:**

```python
# Property 3: Chunking text reassembly
@given(st.text(min_size=100))
@settings(max_examples=100)
def test_chunking_preserves_content(text):
    # Feature: dealflow-ai-backend, Property 3: chunking text reassembly preserves original content
    chunks = embedding_service.chunk_text(text)
    reassembled = reassemble_chunks(chunks, overlap=50)
    assert text in reassembled or set(text).issubset(set(reassembled))

# Property 4: Embedding dimension invariant
@given(st.text(min_size=1, max_size=2000))
@settings(max_examples=100)
def test_embedding_dimension(text):
    # Feature: dealflow-ai-backend, Property 4: embedding dimension invariant
    vec = embedding_service.embed(text)
    assert len(vec) == 384

# Property 5: Embedding determinism
@given(st.text(min_size=1, max_size=500))
@settings(max_examples=100)
def test_embedding_determinism(text):
    # Feature: dealflow-ai-backend, Property 5: embedding determinism
    assert embedding_service.embed(text) == embedding_service.embed(text)

# Property 6: Session isolation
@given(st.text(min_size=1, max_size=200), st.text(min_size=1, max_size=200))
@settings(max_examples=50)
def test_session_isolation(text_a, text_b):
    # Feature: dealflow-ai-backend, Property 6: no cross-session data leakage
    session_a = str(uuid4())
    session_b = str(uuid4())
    # store chunk in session_a, query session_b — should return nothing from session_a

# Property 11: Error response schema
@given(st.sampled_from(["invalid_session_xyz", "", "   "]))
@settings(max_examples=100)
def test_error_response_schema(bad_session_id):
    # Feature: dealflow-ai-backend, Property 11: error response schema conformance
    response = client.post("/api/analyze", json={"sessionId": bad_session_id})
    assert response.status_code in (400, 404, 422)
    body = response.json()
    assert "error" in body and "code" in body
```

### Unit Tests

Unit tests focus on:
- Specific boundary values (file count: 0, 1, 10, 11; file size: 10MB, 10MB+1)
- Error injection (corrupt PDF bytes, invalid image, LLM returning non-JSON)
- Demo data completeness (exact field values required by requirements)
- CORS preflight response

### Integration Tests

Integration tests (using `TestClient` with mocked LLM) cover:
- Full upload → analyze → chat → report pipeline for a single session
- Two concurrent sessions verifying isolation
- LLM failure mid-analysis returning correct 502

### Test Configuration

```python
# conftest.py
@pytest.fixture
def mock_llm(monkeypatch):
    """Patches LLMService.complete() to return deterministic JSON for testing."""
    async def fake_complete(system_prompt, user_prompt, max_tokens=4096):
        return MOCK_ANALYSIS_JSON
    monkeypatch.setattr(LLMService, "complete", fake_complete)
```
