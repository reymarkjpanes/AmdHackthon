"""
Property-based and unit tests for EmbeddingService.
"""

import os
import sys

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Module-level embedding service for use with @given (avoids fixture conflict)
from services.embedding_service import EmbeddingService as _EmbeddingService

_ES = None

def _get_es():
    global _ES
    if _ES is None:
        _ES = _EmbeddingService()
    return _ES


# ---- Property 4: Embedding dimension invariant ----

# Feature: dealflow-ai-backend, Property 4: embedding dimension invariant
@given(st.text(min_size=1, max_size=2000, alphabet=st.characters(blacklist_categories=("Cs",))))
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_embedding_dimension(text):
    """
    Property 4: Embedding dimension invariant.
    Validates: Requirements 1.9, 11.5

    For any text, the embedding vector must have exactly 384 dimensions.
    """
    vec = _get_es().embed(text)
    assert len(vec) == 384, (
        f"Expected 384-dim embedding, got {len(vec)}"
    )


# ---- Property 5: Embedding determinism ----

# Feature: dealflow-ai-backend, Property 5: embedding determinism
@given(st.text(min_size=1, max_size=500, alphabet=st.characters(blacklist_categories=("Cs",))))
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_embedding_determinism(text):
    """
    Property 5: Embedding determinism.
    Validates: Requirements 11.6

    Calling embed() twice with the same input produces identical vectors.
    """
    es = _get_es()
    vec1 = es.embed(text)
    vec2 = es.embed(text)
    assert vec1 == vec2, "embed() is not deterministic for the same input"


# ---- Unit tests ----

def test_embed_returns_list_of_floats():
    """embed() should return a list of floats."""
    vec = _get_es().embed("Hello world")
    assert isinstance(vec, list)
    assert all(isinstance(x, float) for x in vec)


def test_embed_batch_returns_correct_count():
    """embed_batch() should return one vector per input text."""
    texts = ["First text", "Second text", "Third text"]
    vecs = _get_es().embed_batch(texts)
    assert len(vecs) == 3
    for v in vecs:
        assert len(v) == 384


def test_embed_batch_empty():
    """embed_batch() with empty list returns empty list."""
    result = _get_es().embed_batch([])
    assert result == []


def test_embed_batch_single():
    """embed_batch() with single text returns one 384-dim vector."""
    result = _get_es().embed_batch(["test"])
    assert len(result) == 1
    assert len(result[0]) == 384


def test_embed_different_texts_produce_different_vectors():
    """Different texts should produce different embeddings."""
    es = _get_es()
    vec1 = es.embed("apple orange fruit")
    vec2 = es.embed("contract legal obligation payment")
    assert vec1 != vec2


def test_chunk_text_overlap_preserves_words():
    """Overlapping chunks should contain shared words at boundaries."""
    es = _get_es()
    # Create text that forces multiple chunks
    words = [f"word{i}" for i in range(100)]
    text = " ".join(words)
    chunks = es.chunk_text(text, max_tokens=20, overlap=5)

    if len(chunks) >= 2:
        # The end of chunk 0 and start of chunk 1 should overlap
        chunk0_words = set(chunks[0].split())
        chunk1_words = set(chunks[1].split())
        # There should be some overlap
        overlap = chunk0_words & chunk1_words
        assert len(overlap) > 0, "Consecutive chunks should have overlapping words"
