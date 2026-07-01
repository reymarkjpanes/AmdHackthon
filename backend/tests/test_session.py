"""
Tests for SessionManager and VectorStore session isolation.
"""

import os
import sys
import uuid
from datetime import datetime

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.document import Chunk, ProcessingStatus, UploadedDocument


def make_doc(filename: str = "test.pdf") -> UploadedDocument:
    return UploadedDocument(
        id=str(uuid.uuid4()),
        filename=filename,
        fileType="pdf",
        fileSize=1000,
        uploadedAt=datetime.utcnow(),
        processingStatus=ProcessingStatus.COMPLETED,
    )


def make_chunk(text: str, source: str, embedding: list[float]) -> Chunk:
    return Chunk(
        id=str(uuid.uuid4()),
        text=text,
        embedding=embedding,
        source_document=source,
        document_type="pdf",
        chunk_index=0,
    )


# ---- Property 6: Session isolation ----

# Module-level singletons for use in @given tests (avoids reloading model per example)
_ES_FOR_ISOLATION = None
_VS_FOR_ISOLATION = None


def _get_es_for_isolation():
    global _ES_FOR_ISOLATION
    if _ES_FOR_ISOLATION is None:
        from services.embedding_service import EmbeddingService
        _ES_FOR_ISOLATION = EmbeddingService()
    return _ES_FOR_ISOLATION


# Feature: dealflow-ai-backend, Property 6: session isolation — no cross-session data leakage
@given(
    st.text(min_size=1, max_size=200, alphabet=st.characters(blacklist_categories=("Cs",))),
    st.text(min_size=1, max_size=200, alphabet=st.characters(blacklist_categories=("Cs",))),
)
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_session_isolation(text_a, text_b):
    """
    Property 6: Session isolation — no cross-session data leakage.
    Validates: Requirements 9.4, 9.7

    Querying session B should never return chunks stored in session A.
    Uses module-level embedding service to avoid pytest fixture conflict with @given.
    """
    from services.vector_store import VectorStore, reset_client
    reset_client()  # Reset to get fresh client for this example
    vs = VectorStore()
    es = _get_es_for_isolation()
    session_a = str(uuid.uuid4())
    session_b = str(uuid.uuid4())

    # Store chunk in session A
    embedding_a = es.embed(text_a)
    chunk_a = make_chunk(text_a, "doc_a.pdf", embedding_a)
    vs.add_chunks(session_a, [chunk_a])

    # Query session B with session A's embedding — should return nothing from A
    results = vs.query_top_k(session_b, embedding_a, k=5)

    # Session B is empty, should return no results
    assert len(results) == 0, (
        f"Session B returned {len(results)} results from session A's data — isolation violated!"
    )


# ---- SessionManager unit tests ----

def test_create_session(session_manager):
    """create_session should store session with documents."""
    session_id = str(uuid.uuid4())
    docs = [make_doc("test.pdf")]
    session = session_manager.create_session(session_id, docs)

    assert session.session_id == session_id
    assert len(session.documents) == 1
    assert session.analysis is None


def test_get_session_exists(session_manager):
    """get_session should return session when it exists."""
    session_id = str(uuid.uuid4())
    session_manager.create_session(session_id, [make_doc()])
    session = session_manager.get_session(session_id)
    assert session.session_id == session_id


def test_get_session_not_found(session_manager):
    """get_session should raise SessionNotFoundError for unknown IDs."""
    from services.session_manager import SessionNotFoundError
    with pytest.raises(SessionNotFoundError):
        session_manager.get_session("nonexistent-session-id")


def test_session_exists_true(session_manager):
    """session_exists returns True for created sessions."""
    session_id = str(uuid.uuid4())
    session_manager.create_session(session_id, [make_doc()])
    assert session_manager.session_exists(session_id) is True


def test_session_exists_false(session_manager):
    """session_exists returns False for unknown IDs."""
    assert session_manager.session_exists("unknown-id-xyz") is False


def test_store_analysis(session_manager):
    """store_analysis should attach analysis to session."""
    from models.response import AnalysisResult, Recommendation
    from datetime import datetime

    session_id = str(uuid.uuid4())
    session_manager.create_session(session_id, [make_doc()])

    analysis = AnalysisResult(
        analyzedAt=datetime.utcnow(),
        executiveSummary="Test summary",
        risks=[],
        comparisonMatrix=[],
        conflicts=[],
        recommendation=Recommendation(
            title="Test", summary="Test", nextSteps=["step1"], confidence=0.9
        ),
    )

    session_manager.store_analysis(session_id, analysis)
    session = session_manager.get_session(session_id)
    assert session.analysis is not None
    assert session.analysis.executiveSummary == "Test summary"


def test_multiple_sessions_independent(session_manager):
    """Multiple sessions should be independent."""
    ids = [str(uuid.uuid4()) for _ in range(5)]
    for sid in ids:
        session_manager.create_session(sid, [make_doc(f"doc_{sid[:8]}.pdf")])

    for sid in ids:
        session = session_manager.get_session(sid)
        assert session.session_id == sid
        assert session.documents[0].filename == f"doc_{sid[:8]}.pdf"


# ---- VectorStore unit tests ----

def test_vector_store_add_and_retrieve(vector_store, embedding_service):
    """add_chunks and get_all_chunks should round-trip correctly."""
    session_id = str(uuid.uuid4())
    text = "Procurement document with supplier data."
    embedding = embedding_service.embed(text)
    chunk = make_chunk(text, "test.pdf", embedding)

    vector_store.add_chunks(session_id, [chunk])
    retrieved = vector_store.get_all_chunks(session_id)

    assert len(retrieved) == 1
    assert retrieved[0].text == text
    assert retrieved[0].source_document == "test.pdf"


def test_vector_store_query_top_k(vector_store, embedding_service):
    """query_top_k should return the most similar chunks."""
    session_id = str(uuid.uuid4())
    texts = [
        "Supplier A offers competitive pricing at $45,200.",
        "The procurement policy requires three bids.",
        "Contract renewal deadline is June 30, 2026.",
    ]
    embeddings = embedding_service.embed_batch(texts)
    chunks = [make_chunk(t, f"doc{i}.pdf", e) for i, (t, e) in enumerate(zip(texts, embeddings))]
    vector_store.add_chunks(session_id, chunks)

    # Query for pricing-related text
    query_embedding = embedding_service.embed("price cost budget")
    results = vector_store.query_top_k(session_id, query_embedding, k=2)

    assert len(results) <= 2
    assert len(results) >= 1


def test_vector_store_collection_exists(vector_store, embedding_service):
    """collection_exists should return True after chunks are added."""
    session_id = str(uuid.uuid4())
    assert vector_store.collection_exists(session_id) is False

    text = "Test document content."
    embedding = embedding_service.embed(text)
    chunk = make_chunk(text, "test.pdf", embedding)
    vector_store.add_chunks(session_id, [chunk])

    assert vector_store.collection_exists(session_id) is True


def test_vector_store_empty_session(vector_store):
    """get_all_chunks on empty session should return empty list."""
    session_id = str(uuid.uuid4())
    chunks = vector_store.get_all_chunks(session_id)
    assert chunks == []
