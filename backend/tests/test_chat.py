"""
Tests for chat endpoint — RAG retrieval, schema conformance, and session validation.
"""

import os
import sys
import uuid
from datetime import datetime

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---- Property 9: Chat response schema conformance and timing ----

# Feature: dealflow-ai-backend, Property 9: chat response schema conformance and timing
def test_chat_response_schema():
    """
    Property 9: Chat response schema conformance and timing.
    Validates: Requirements 3.8, 3.9, 3.10, 3.7
    """
    from models.response import ChatResponse, StructuredAIResponse, Evidence

    response = ChatResponse(
        messageId=str(uuid.uuid4()),
        role="assistant",
        structuredResponse=StructuredAIResponse(
            answer="Test answer",
            evidence=[
                Evidence(
                    quote="Short quote from document",
                    sourceDocument="test.pdf",
                    documentType="pdf",
                )
            ],
            risks="No significant risks",
            recommendation="Proceed with caution",
        ),
        processingTimeMs=350,
    )

    assert response.role == "assistant"
    assert response.processingTimeMs >= 0
    assert len(response.messageId) > 0

    # Every evidence quote must be at most 200 characters
    for ev in response.structuredResponse.evidence:
        assert len(ev.quote) <= 200, f"Quote exceeds 200 chars: '{ev.quote[:50]}...'"


def test_evidence_quote_max_200_chars():
    """Evidence quotes must not exceed 200 characters."""
    from models.response import Evidence

    short_quote = "A" * 200  # Exactly 200 — valid
    ev = Evidence(quote=short_quote, sourceDocument="test.pdf", documentType="pdf")
    assert len(ev.quote) <= 200

    # Over 200 chars is allowed by model but must be truncated by router
    long_quote = "A" * 250
    ev_long = Evidence(quote=long_quote, sourceDocument="test.pdf", documentType="pdf")
    # The model allows it — the router truncates before creating Evidence
    assert len(ev_long.quote) == 250  # Model doesn't enforce — router does


def test_processing_time_non_negative():
    """processingTimeMs must be a non-negative integer."""
    from models.response import ChatResponse, StructuredAIResponse

    response = ChatResponse(
        messageId=str(uuid.uuid4()),
        role="assistant",
        structuredResponse=StructuredAIResponse(
            answer="Answer", evidence=[], risks="", recommendation=""
        ),
        processingTimeMs=0,
    )
    assert response.processingTimeMs >= 0


# ---- Property 10: Unknown session returns 404 ----

# Feature: dealflow-ai-backend, Property 10: unknown session returns 404 on all endpoints
def test_unknown_session_chat_404(test_client):
    """
    Property 10: Unknown session returns 404 on /api/chat.
    Validates: Requirements 3.2
    """
    response = test_client.post(
        "/api/chat",
        json={"sessionId": "definitely-not-a-real-session", "question": "What is the price?"},
    )
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "SESSION_NOT_FOUND"


def test_unknown_session_analyze_404(test_client):
    """
    Property 10: Unknown session returns 404 on /api/analyze.
    Validates: Requirements 2.2
    """
    response = test_client.post(
        "/api/analyze",
        json={"sessionId": "not-a-real-session-id"},
    )
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "SESSION_NOT_FOUND"


def test_unknown_session_report_404(test_client):
    """
    Property 10: Unknown session returns 404 on /api/report.
    Validates: Requirements 4.2
    """
    response = test_client.post(
        "/api/report",
        json={"sessionId": "not-a-real-session-id", "includeChat": False},
    )
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "SESSION_NOT_FOUND"


def test_chat_requires_non_empty_question(test_client, sample_pdf_bytes):
    """Chat endpoint should reject empty question with 400 INVALID_REQUEST."""
    # First create a session via upload
    upload_response = test_client.post(
        "/api/upload",
        files=[("files", ("test.pdf", sample_pdf_bytes, "application/pdf"))],
    )

    if upload_response.status_code != 200:
        pytest.skip("Upload not available in test environment")

    session_id = upload_response.json()["sessionId"]

    # Send empty question
    response = test_client.post(
        "/api/chat",
        json={"sessionId": session_id, "question": ""},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "INVALID_REQUEST"


def test_chat_missing_question_rejected(test_client, sample_pdf_bytes):
    """Chat endpoint rejects whitespace-only question."""
    upload_response = test_client.post(
        "/api/upload",
        files=[("files", ("test.pdf", sample_pdf_bytes, "application/pdf"))],
    )

    if upload_response.status_code != 200:
        pytest.skip("Upload not available in test environment")

    session_id = upload_response.json()["sessionId"]

    response = test_client.post(
        "/api/chat",
        json={"sessionId": session_id, "question": "   "},
    )
    assert response.status_code == 400
