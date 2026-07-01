# Implementation Plan: DealFlow AI Backend

## Overview

Implement a FastAPI (Python 3.11) service that exposes five REST endpoints consumed by the existing Next.js frontend. The service is structured with `routers/`, `services/`, `models/`, and `prompts/` packages, uses ChromaDB in-memory for vector storage, `sentence-transformers` for embeddings, Anthropic Claude (or AMD Developer Cloud) for LLM inference, and ReportLab for PDF export. All JSON field names and HTTP status codes must exactly match the contracts defined in `dealflow-ai-frontend/lib/api.ts` and `lib/types.ts`.

## Tasks

- [x] 1. Set up project structure, dependencies, and configuration
  - Create `backend/` directory with `main.py`, `routers/`, `services/`, `models/`, `prompts/`, `tests/` packages (each with `__init__.py`)
  - Write `requirements.txt` with pinned versions for: `fastapi`, `uvicorn[standard]`, `python-multipart`, `pymupdf`, `pytesseract`, `Pillow`, `sentence-transformers`, `chromadb`, `anthropic`, `reportlab`, `python-dotenv`, `pydantic`, `pytest`, `pytest-asyncio`, `httpx`, `hypothesis`, `pytest-mock`
  - Write `.env.example` documenting `ANTHROPIC_API_KEY`, `AMD_CLOUD_API_KEY`, `AMD_CLOUD_ENDPOINT`, `LLM_PROVIDER`, `ALLOWED_ORIGINS`, `PORT`
  - Write `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 2. Implement Pydantic data models
  - [x] 2.1 Create `models/document.py` with `ProcessingStatus` enum, `UploadedDocument`, and `Chunk` models
    - `ProcessingStatus` values: `uploading`, `uploaded`, `extracting_text`, `running_ocr`, `generating_embeddings`, `indexing`, `completed`, `failed`
    - `UploadedDocument`: `id` (UUID str), `filename`, `fileType` (`"pdf"|"image"`), `fileSize` (int), `uploadedAt` (datetime), `processingStatus`
    - `Chunk`: `id`, `text`, `embedding` (list[float]), `source_document`, `document_type`, `chunk_index`
    - _Requirements: 1.12_

  - [x] 2.2 Create `models/response.py` with all request/response envelope models
    - `Risk`, `Conflict`, `ComparisonRow`, `Recommendation`, `AnalysisResult`, `Evidence`, `StructuredAIResponse`
    - Request/response envelopes: `UploadResponse`, `AnalyzeRequest`, `AnalyzeResponse`, `ChatRequest`, `ChatResponse`, `ReportRequest`, `ErrorResponse`
    - Set `model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})` on all models with datetime fields
    - _Requirements: 1.11, 2.9, 2.10, 3.8, 3.9, 4.1, 5.2, 8.1_

- [x] 3. Implement core services
  - [x] 3.1 Create `services/document_parser.py` — `DocumentParser` class
    - `extract_text(file_bytes, mime_type) -> str`: dispatch to PDF or image extraction
    - `_extract_pdf(file_bytes) -> str`: use `fitz` (PyMuPDF) page by page; fall back to `pytesseract` for image-only pages
    - `_extract_image(file_bytes) -> str`: use `pytesseract` + `Pillow`
    - Raise `ExtractionError` on unrecoverable failure
    - _Requirements: 1.6, 1.7, 11.1, 11.2_

  - [ ]* 3.2 Write property test for chunking text reassembly (Property 3)
    - **Property 3: Chunking text reassembly preserves original content**
    - **Validates: Requirements 1.8, 11.3**
    - Use `hypothesis` `@given(st.text(min_size=100))` with `@settings(max_examples=100)`
    - Reassemble chunks by deduplicating overlap and assert original content is a subset
    - File: `tests/test_upload.py`

  - [x] 3.3 Create `services/embedding_service.py` — `EmbeddingService` class
    - Load `SentenceTransformer("all-MiniLM-L6-v2")` at init (AMD: ROCm GPU-accelerated)
    - `embed(text: str) -> list[float]`: return 384-dim vector
    - `embed_batch(texts: list[str]) -> list[list[float]]`: batch encoding for AMD MI300X efficiency
    - `chunk_text(text, max_tokens=512, overlap=50) -> list[str]`: overlapping token-based chunking
    - _Requirements: 1.8, 1.9, 3.4, 11.3, 11.4, 11.5, 11.6_

  - [ ]* 3.4 Write property tests for embedding service (Properties 4 and 5)
    - **Property 4: Embedding dimension invariant** — `@given(st.text(min_size=1, max_size=2000))`, assert `len(vec) == 384`
    - **Property 5: Embedding determinism** — `@given(st.text(min_size=1, max_size=500))`, assert two calls produce identical vectors
    - **Validates: Requirements 1.9, 11.5, 11.6**
    - File: `tests/test_embedding.py`

  - [x] 3.5 Create `services/vector_store.py` — `VectorStore` class
    - Use `chromadb.EphemeralClient()` (in-memory)
    - `create_collection(session_id)`, `add_chunks(session_id, chunks)`, `query_top_k(session_id, embedding, k=5) -> list[Chunk]`
    - `get_all_chunks(session_id) -> list[Chunk]`, `collection_exists(session_id) -> bool`
    - _Requirements: 1.10, 3.5, 9.1, 9.3_

  - [ ]* 3.6 Write property test for session isolation (Property 6)
    - **Property 6: Session isolation — no cross-session data leakage**
    - **Validates: Requirements 9.4, 9.7**
    - `@given(st.text(min_size=1, max_size=200), st.text(min_size=1, max_size=200))` with `@settings(max_examples=50)`
    - Create two sessions, store chunk in session A, query session B — assert no results from session A returned
    - File: `tests/test_session.py`

  - [x] 3.7 Create `services/session_manager.py` — `SessionManager` class
    - `SessionData` dataclass with `session_id`, `documents`, `analysis`, `created_at`
    - In-memory `dict[str, SessionData]` store
    - `create_session`, `get_session` (raise `SessionNotFoundError`), `store_analysis`, `session_exists`
    - _Requirements: 1.5, 9.2, 9.4, 9.5, 9.6_

  - [x] 3.8 Create `services/llm_service.py` — `LLMService` class
    - `LLMProvider` enum: `CLAUDE`, `AMD`
    - Read `LLM_PROVIDER` env var, default to `CLAUDE`; raise `ConfigurationError` at startup if `CLAUDE` and `ANTHROPIC_API_KEY` missing
    - `async complete(system_prompt, user_prompt, max_tokens=4096) -> str`; AMD stub returns mock if `AMD_CLOUD_ENDPOINT` not configured
    - Log active provider at startup
    - `_parse_with_retry(prompt, model_class)`: attempt parse, retry once with corrective instruction on `ValidationError`, raise `LLMParseError` on second failure
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 12.6_

  - [ ]* 3.9 Write property test for LLM provider routing (Property 12)
    - **Property 12: LLM provider routing**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
    - Mock `LLMService.complete()` and assert non-empty string returned; assert provider matches `LLM_PROVIDER` env var
    - File: `tests/test_analysis.py`

- [ ] 4. Checkpoint — Ensure all service unit tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement prompt templates
  - [x] 5.1 Create `prompts/system_prompt.py` — `get_system_prompt(doc_list) -> str`
    - Identify assistant as AMD MI300X-powered procurement analyst
    - _Requirements: 12.1, 12.7_

  - [x] 5.2 Create `prompts/executive_summary.py`, `prompts/risk_analysis.py`, `prompts/recommendation.py`
    - `build_summary_prompt(chunks) -> str`: return JSON `{"executiveSummary": str}`
    - `build_risk_prompt(chunks) -> str`: return JSON `{"risks": [...]}` with `HIGH`/`MEDIUM`/`LOW` only
    - `build_recommendation_prompt(chunks) -> str`: return JSON `{title, summary, nextSteps, confidence}`
    - _Requirements: 12.1, 12.2, 12.3_

  - [x] 5.3 Create `prompts/conflict_detection.py` — `build_conflict_prompt(doc_a, doc_b) -> str`
    - Pairwise comparison, return JSON array of conflict objects
    - Instruct LLM to identify only factual contradictions, not stylistic differences
    - _Requirements: 12.1, 12.2, 12.4_

  - [x] 5.4 Create `prompts/chat_copilot.py` — `build_chat_prompt(question, chunks) -> str`
    - RAG prompt grounding every claim in verbatim Chunk quote
    - Return JSON `{answer, evidence, risks, recommendation}`; `sourceDocument` = exact filename
    - _Requirements: 12.1, 12.2, 12.5_

- [x] 6. Implement analysis and conflict services
  - [x] 6.1 Create `services/conflict_engine.py` — `ConflictEngine` class
    - `async detect(chunks, document_names) -> list[Conflict]`
    - Compare documents pairwise using `build_conflict_prompt`; parse result into `list[Conflict]`
    - _Requirements: 2.7_

  - [x] 6.2 Create `services/analysis_service.py` — `AnalysisService` class
    - `async run_full_analysis(session_id, chunks, doc_names) -> AnalysisResult`
    - Orchestrate 4 LLM calls (summary, risks, comparison matrix, recommendation) + `ConflictEngine.detect` in parallel where possible
    - Store result via `SessionManager.store_analysis`
    - _Requirements: 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 2.12_

  - [ ]* 6.3 Write property test for analysis response schema conformance (Property 7)
    - **Property 7: Analysis response schema conformance**
    - **Validates: Requirements 2.9, 2.10**
    - With mocked LLM, call `/api/analyze`, assert HTTP 200, assert response deserializes into `AnalyzeResponse` with `status="completed"` and non-null `analysis` containing all required sub-fields
    - File: `tests/test_analysis.py`

  - [ ]* 6.4 Write property test for risk level constraint (Property 8)
    - **Property 8: Risk level constraint**
    - **Validates: Requirements 2.5, 12.3**
    - Assert every risk in `AnalysisResult.risks` has `level` in `{"HIGH", "MEDIUM", "LOW"}`
    - File: `tests/test_analysis.py`

- [x] 7. Implement PDF report generator
  - [x] 7.1 Create `services/pdf_generator.py` — `PDFGenerator` class
    - `AMD_RED = "#ED1C24"`
    - `generate_report(analysis, session_id) -> bytes` using ReportLab
    - Sections: title page ("DealFlow AI — Document Intelligence Report", timestamp, "Powered by AMD MI300X"), executive summary, risk table, comparison matrix table, conflicts, recommendation with numbered next steps and confidence %
    - _Requirements: 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9_

  - [ ]* 7.2 Write property test for PDF report headers (Property 13)
    - **Property 13: PDF report header fields**
    - **Validates: Requirements 4.10**
    - Assert `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="dealflow-report-YYYY-MM-DD.pdf"` regex match on valid report response
    - File: `tests/test_analysis.py`

- [x] 8. Implement routers
  - [x] 8.1 Create `routers/upload.py` — `POST /api/upload`
    - Validate MIME type (`application/pdf`, `image/png`, `image/jpeg`) → HTTP 400 `UNSUPPORTED_FORMAT` otherwise
    - Validate file count (1–10) → HTTP 400 `FILE_COUNT_EXCEEDED`; validate file size (≤10 MB) → HTTP 400 `FILE_SIZE_EXCEEDED`
    - Per-file try/except: set `processingStatus = "failed"` on error; if all fail → HTTP 422 `UPLOAD_FAILED`
    - Pipeline: `DocumentParser.extract_text` → `EmbeddingService.chunk_text` → `EmbeddingService.embed_batch` → `VectorStore.add_chunks` → `SessionManager.create_session`
    - Return `UploadResponse` (HTTP 200)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12, 1.13, 1.14_

  - [ ]* 8.2 Write property tests for MIME type acceptance (Property 1) and file size/count boundaries
    - **Property 1: MIME type acceptance is exhaustive and exclusive**
    - **Validates: Requirements 1.2**
    - `@given(st.text())` — assert accepted iff MIME is `application/pdf`, `image/png`, `image/jpeg`; others → HTTP 400 `UNSUPPORTED_FORMAT`
    - Unit tests: file count 0, 1, 10, 11; file size exactly 10 MB and 10 MB + 1 byte
    - File: `tests/test_upload.py`

  - [x] 8.3 Create `routers/analyze.py` — `POST /api/analyze`
    - Validate `sessionId` → HTTP 404 `SESSION_NOT_FOUND` if not found
    - Call `AnalysisService.run_full_analysis`; on `LLMParseError` → HTTP 502 `ANALYSIS_FAILED`
    - Return `AnalyzeResponse` with `status="completed"` (HTTP 200)
    - _Requirements: 2.1, 2.2, 2.3, 2.9, 2.11, 2.12_

  - [x] 8.4 Create `routers/chat.py` — `POST /api/chat`
    - Validate `sessionId` → HTTP 404; validate `question` non-empty → HTTP 400 `INVALID_REQUEST`
    - Embed question → `VectorStore.query_top_k(k=5)` → `build_chat_prompt` → `LLMService.complete`
    - Record `processingTimeMs`; return `ChatResponse` (HTTP 200); LLM failure → HTTP 502 `ANALYSIS_FAILED`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11_

  - [ ]* 8.5 Write property tests for chat response schema and timing (Property 9) and unknown session 404 (Property 10)
    - **Property 9: Chat response schema conformance and timing**
    - **Validates: Requirements 3.8, 3.9, 3.10, 3.7**
    - Assert response deserializes into `ChatResponse`; `processingTimeMs` ≥ 0; each evidence `quote` ≤ 200 chars
    - **Property 10: Unknown session returns 404 on all endpoints**
    - **Validates: Requirements 2.2, 3.2, 4.2**
    - `@given(st.text())` with non-existent session IDs — assert HTTP 404 with `code="SESSION_NOT_FOUND"` on `/api/analyze`, `/api/chat`, `/api/report`
    - File: `tests/test_chat.py`

  - [x] 8.6 Create `routers/report.py` — `POST /api/report`
    - Validate `sessionId` with completed analysis → HTTP 404 `SESSION_NOT_FOUND` if not found
    - Call `PDFGenerator.generate_report`; on failure → HTTP 500 `REPORT_FAILED`
    - Return `StreamingResponse` with `Content-Type: application/pdf`, `Content-Disposition: attachment; filename="dealflow-report-<YYYY-MM-DD>.pdf"`
    - _Requirements: 4.1, 4.2, 4.10, 4.11_

  - [x] 8.7 Create `routers/demo.py` — `GET /api/demo`
    - Return static `DemoData` JSON: 5 documents (`Supplier_A_Quotation.pdf`, `Supplier_B_Quotation.pdf`, `Existing_Contract_TechCorp.pdf`, `Invoice_TechCorp_March2026.pdf`, `Company_Procurement_Policy.pdf`)
    - `analysis.risks`: ≥1 HIGH (invoice overcharge), ≥1 HIGH (contract renewal), ≥1 MEDIUM, ≥1 LOW
    - `comparisonMatrix`: ≥5 rows, Supplier B wins ≥3 fields
    - `conflicts`: ≥2 items, first is HIGH-severity price discrepancy between invoice and contract
    - `recommendation`: Supplier B, `confidence=0.87`, `nextSteps` ≥4 items
    - `preSeededMessages`: ≥4 messages (2 user + 2 assistant turns)
    - All datetimes as valid ISO 8601 strings
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10_

- [x] 9. Implement `main.py` and CORS/global error handling
  - [x] 9.1 Create `main.py` wiring all routers and middleware
    - Instantiate `FastAPI(title="DealFlow AI", version="1.0.0")`
    - Add `CORSMiddleware`: allow all origins (dev) or `ALLOWED_ORIGINS` env var; methods `GET, POST, OPTIONS`; headers `Content-Type, Authorization, X-Requested-With`
    - `app.include_router` for all 5 routers with `/api` prefix
    - Register global exception handler returning `{"error": "...", "code": "UNKNOWN_ERROR", "details": null}` with HTTP 500 — never exposing stack traces
    - Add `GET /health` returning `{"status": "ok", "version": "1.0.0"}`
    - Listen on `0.0.0.0:8000`, overridable via `PORT` env var
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 8.1, 8.7, 10.6_

  - [ ]* 9.2 Write property test for error response schema conformance (Property 11)
    - **Property 11: Error response schema conformance**
    - **Validates: Requirements 8.1, 8.2**
    - For all 4xx and 5xx responses across all endpoints, assert body deserializes into `ErrorResponse` and `code` is in the `API_ERROR_CODES` set
    - File: `tests/test_error_format.py`

  - [ ]* 9.3 Write property test for session creation round-trip (Property 2)
    - **Property 2: Session creation round-trip**
    - **Validates: Requirements 1.5, 9.1, 9.2**
    - For any valid upload (1–10 files, ≤10 MB, accepted MIME), returned `sessionId` is valid UUID v4, and subsequent `/api/analyze` and `/api/chat` calls with it do NOT return 404
    - File: `tests/test_upload.py`

- [ ] 10. Write integration and conflict detection tests
  - [ ]* 10.1 Write integration test covering full upload → analyze → chat → report pipeline
    - Use `TestClient` with mocked LLM (`conftest.py` `mock_llm` fixture patching `LLMService.complete`)
    - Single session: upload → analyze → chat → report; assert each step returns expected status code and schema
    - Two concurrent sessions: assert no cross-session contamination (Property 6)
    - LLM failure mid-analysis: assert HTTP 502 `ANALYSIS_FAILED`
    - File: `tests/test_analysis.py`

  - [ ]* 10.2 Write unit tests for `ConflictEngine` pairwise detection
    - Test that two contradicting document excerpts produce at least one `Conflict` object
    - Test that identical document excerpts produce zero conflicts
    - File: `tests/test_conflict.py`

- [x] 11. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- All JSON field names must exactly match `dealflow-ai-frontend/lib/types.ts` — field name mismatches will silently break the frontend
- The `all-MiniLM-L6-v2` model download (~90 MB) happens at first startup; build systems should pre-cache it
- For local development without AMD credentials, set `LLM_PROVIDER=AMD` — the stub returns mock data
- Each property test is tagged `# Feature: dealflow-ai-backend, Property N: <text>` for traceability
- Checkpoints ensure incremental validation before adding more complexity

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["2.1", "2.2"] },
    { "id": 1, "tasks": ["3.1", "3.3", "3.5", "3.7", "3.8"] },
    { "id": 2, "tasks": ["3.2", "3.4", "3.6", "3.9", "5.1", "5.2", "5.3", "5.4"] },
    { "id": 3, "tasks": ["6.1", "6.2"] },
    { "id": 4, "tasks": ["6.3", "6.4", "7.1"] },
    { "id": 5, "tasks": ["7.2", "8.1", "8.3", "8.4", "8.6", "8.7"] },
    { "id": 6, "tasks": ["8.2", "8.5", "9.1"] },
    { "id": 7, "tasks": ["9.2", "9.3", "10.2"] },
    { "id": 8, "tasks": ["10.1"] }
  ]
}
```
