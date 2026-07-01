"""
Shared test fixtures for DealFlow AI backend tests.

NOTE: numpy is available via the sentence-transformers dependency — no extra install needed.
The embedding_service fixture uses a mock to avoid loading the real model (15-20s startup).
"""

import asyncio
import json
import os
import sys
import uuid
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Ensure backend/ is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set minimal environment for tests — use AMD stub mode to avoid needing API keys
os.environ.setdefault("LLM_PROVIDER", "AMD")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-used-in-stub-mode")


# ---- Mock LLM JSON responses ----
MOCK_SUMMARY_JSON = json.dumps({"executiveSummary": "Test summary of procurement documents."})

MOCK_RISKS_JSON = json.dumps({
    "risks": [
        {"id": "r1", "level": "HIGH", "description": "Test high risk", "sourceDocument": "test.pdf", "category": "Financial"},
        {"id": "r2", "level": "MEDIUM", "description": "Test medium risk", "sourceDocument": "test.pdf", "category": "Legal"},
        {"id": "r3", "level": "LOW", "description": "Test low risk", "sourceDocument": "test.pdf", "category": "Operational"},
    ]
})

MOCK_MATRIX_JSON = json.dumps({
    "comparisonMatrix": [
        {"field": "Price", "values": {"Supplier A": "$100", "Supplier B": "$90"}, "winner": "Supplier B"},
        {"field": "Terms", "values": {"Supplier A": "Net 30", "Supplier B": "Net 60"}, "winner": "Supplier B"},
        {"field": "Delivery", "values": {"Supplier A": "7 days", "Supplier B": "14 days"}, "winner": "Supplier A"},
        {"field": "Warranty", "values": {"Supplier A": "1 year", "Supplier B": "2 years"}, "winner": "Supplier B"},
        {"field": "SLA", "values": {"Supplier A": "48h", "Supplier B": "24h"}, "winner": "Supplier B"},
    ]
})

MOCK_RECOMMENDATION_JSON = json.dumps({
    "title": "Proceed with Supplier B",
    "summary": "Supplier B offers the best value.",
    "nextSteps": ["Step 1", "Step 2", "Step 3", "Step 4"],
    "confidence": 0.87,
})

MOCK_CONFLICTS_JSON = json.dumps([
    {
        "id": "c1",
        "type": "Price Discrepancy",
        "severity": "HIGH",
        "documentA": {"name": "invoice.pdf", "excerpt": "Total: $500"},
        "documentB": {"name": "contract.pdf", "excerpt": "Agreed price: $450"},
        "explanation": "Invoice exceeds agreed contract price.",
        "recommendedAction": "Request itemized breakdown.",
    }
])

MOCK_CHAT_JSON = json.dumps({
    "answer": "Based on the documents, Supplier B is recommended.",
    "evidence": [
        {"quote": "Supplier B price: $42,800", "sourceDocument": "supplier_b.pdf", "documentType": "pdf"}
    ],
    "risks": "Ensure compliance with procurement policy.",
    "recommendation": "Proceed with Supplier B after obtaining third quote.",
})

MOCK_ANALYSIS_JSON = json.dumps({
    "executiveSummary": "Test executive summary.",
    "risks": [
        {"id": "r1", "level": "HIGH", "description": "Risk 1", "sourceDocument": "test.pdf", "category": "Financial"},
        {"id": "r2", "level": "MEDIUM", "description": "Risk 2", "sourceDocument": "test.pdf", "category": "Legal"},
    ],
    "comparisonMatrix": [
        {"field": "Price", "values": {"A": "$100", "B": "$90"}, "winner": "B"},
    ],
    "conflicts": [],
    "recommendation": {
        "title": "Proceed with B",
        "summary": "B is better.",
        "nextSteps": ["Step 1", "Step 2", "Step 3", "Step 4"],
        "confidence": 0.85,
    },
})


def get_mock_llm_response(system_prompt: str = "", user_prompt: str = "") -> str:
    """Return appropriate mock JSON based on prompt content."""
    combined = (user_prompt + system_prompt).lower()
    if "executivesummary" in combined or "executive summary" in combined:
        return MOCK_SUMMARY_JSON
    elif '"risks"' in combined or "risk" in combined and "comparison" not in combined:
        return MOCK_RISKS_JSON
    elif "comparisonmatrix" in combined or "comparison matrix" in combined:
        return MOCK_MATRIX_JSON
    elif "recommendation" in combined and "nextSteps" in user_prompt:
        return MOCK_RECOMMENDATION_JSON
    elif "answer" in combined and "evidence" in combined:
        return MOCK_CHAT_JSON
    elif '"conflicts"' in combined or "conflict" in combined:
        return MOCK_CONFLICTS_JSON
    else:
        return MOCK_ANALYSIS_JSON


@pytest.fixture(scope="session")
def mock_llm_complete():
    """Async mock for LLMService.complete()."""
    async def fake_complete(
        system_prompt: str = "",
        user_prompt: str = "",
        max_tokens: int = 4096,
    ) -> str:
        return get_mock_llm_response(system_prompt, user_prompt)

    return fake_complete


@pytest.fixture(scope="session")
def embedding_service():
    """Mocked EmbeddingService — returns deterministic fake embeddings, no model load."""
    from unittest.mock import MagicMock
    import numpy as np

    mock_svc = MagicMock()
    mock_svc.model = MagicMock()

    def fake_embed(text: str) -> list:
        """Deterministic fake embedding based on text hash."""
        import hashlib
        h = int(hashlib.md5(text.encode()).hexdigest(), 16)
        rng = np.random.RandomState(h % (2**32))
        vec = rng.randn(384).astype(np.float32)
        vec = vec / np.linalg.norm(vec)
        return vec.tolist()

    def fake_embed_batch(texts: list) -> list:
        return [fake_embed(t) for t in texts]

    def fake_chunk_text(text: str, max_tokens: int = 512, overlap: int = 50) -> list:
        """Simple word-based chunking for tests."""
        if not text or not text.strip():
            return []
        words = text.split()
        max_words = int(max_tokens * 0.75)
        if len(words) <= max_words:
            return [text]
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunks.append(" ".join(words[start:end]))
            start += max_words - int(overlap * 0.75)
            if start >= len(words):
                break
        return chunks

    mock_svc.embed = fake_embed
    mock_svc.embed_batch = fake_embed_batch
    mock_svc.chunk_text = fake_chunk_text

    return mock_svc


@pytest.fixture(scope="function")
def vector_store(tmp_path):
    """Fresh VectorStore instance per test — uses an isolated tmp directory."""
    import services.vector_store as vs_module
    # Point to a temp dir so tests never touch the real data/chroma
    vs_module._CHROMA_DIR = str(tmp_path / "chroma")
    vs_module._shared_client = None
    yield vs_module.VectorStore()
    # Cleanup
    vs_module._shared_client = None


@pytest.fixture(scope="function")
def session_manager(tmp_path):
    """Fresh SessionManager instance per test — uses an isolated tmp directory."""
    import services.session_manager as sm_module
    original = sm_module._PERSIST_DIR
    sm_module._PERSIST_DIR = str(tmp_path / "sessions")
    os.makedirs(sm_module._PERSIST_DIR, exist_ok=True)
    from services.session_manager import SessionManager
    yield SessionManager()
    sm_module._PERSIST_DIR = original


@pytest.fixture(scope="function")
def document_parser():
    """DocumentParser instance."""
    from services.document_parser import DocumentParser
    return DocumentParser()


@pytest.fixture(scope="function")
def test_client(mock_llm_complete, embedding_service):
    """
    FastAPI TestClient with mocked LLM and embedding services.
    No real models are loaded — all AI calls return deterministic mock data.
    """
    from unittest.mock import AsyncMock, patch, MagicMock

    mock_embedding_cls = MagicMock(return_value=embedding_service)

    with patch("services.llm_service.LLMService.complete", new=mock_llm_complete), \
         patch("services.embedding_service.EmbeddingService", mock_embedding_cls):
        from main import app
        with TestClient(app, raise_server_exceptions=False) as client:
            yield client


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Generate a minimal valid PDF as bytes for testing."""
    # Minimal PDF structure
    return b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 100 700 Td (Test PDF content) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000266 00000 n
0000000360 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
441
%%EOF"""


@pytest.fixture
def sample_session_id() -> str:
    """Generate a test session ID."""
    return str(uuid.uuid4())
