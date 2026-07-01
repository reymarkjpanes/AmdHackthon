"""
Tests for error response schema conformance across all endpoints.
Property 11: Error response schema conformance.
"""

import os
import sys

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# All valid error codes from the frontend's api.ts
API_ERROR_CODES = {
    "FILE_SIZE_EXCEEDED",
    "FILE_COUNT_EXCEEDED",
    "UNSUPPORTED_FORMAT",
    "UPLOAD_FAILED",
    "ANALYSIS_FAILED",
    "SESSION_NOT_FOUND",
    "NETWORK_ERROR",
    "UNAUTHORIZED",
    "UNKNOWN_ERROR",
    "INVALID_REQUEST",
    "REPORT_FAILED",
}


def assert_error_response(body: dict, expected_code: str | None = None):
    """Assert that a response body is a valid ErrorResponse."""
    assert "error" in body, f"Missing 'error' field in: {body}"
    assert "code" in body, f"Missing 'code' field in: {body}"
    assert isinstance(body["error"], str), "error field must be a string"
    assert isinstance(body["code"], str), "code field must be a string"
    assert body["code"] in API_ERROR_CODES, (
        f"Unknown error code '{body['code']}'. "
        f"Expected one of: {API_ERROR_CODES}"
    )
    if expected_code:
        assert body["code"] == expected_code, (
            f"Expected code '{expected_code}', got '{body['code']}'"
        )


# ---- Property 11: Error response schema conformance ----

# Feature: dealflow-ai-backend, Property 11: error response schema conformance
def test_session_not_found_error_schema(test_client):
    """
    Property 11: Error response schema on /api/analyze with unknown session.
    Validates: Requirements 8.1, 8.2
    """
    response = test_client.post(
        "/api/analyze",
        json={"sessionId": "nonexistent-session"},
    )
    assert response.status_code == 404
    assert_error_response(response.json(), "SESSION_NOT_FOUND")


def test_chat_session_not_found_error_schema(test_client):
    """Error schema on /api/chat with unknown session."""
    response = test_client.post(
        "/api/chat",
        json={"sessionId": "nonexistent-session", "question": "test"},
    )
    assert response.status_code == 404
    assert_error_response(response.json(), "SESSION_NOT_FOUND")


def test_report_session_not_found_error_schema(test_client):
    """Error schema on /api/report with unknown session."""
    response = test_client.post(
        "/api/report",
        json={"sessionId": "nonexistent-session", "includeChat": False},
    )
    assert response.status_code == 404
    assert_error_response(response.json(), "SESSION_NOT_FOUND")


def test_upload_unsupported_mime_error_schema(test_client):
    """Error schema on /api/upload with unsupported MIME type."""
    response = test_client.post(
        "/api/upload",
        files=[("files", ("test.txt", b"text content", "text/plain"))],
    )
    assert response.status_code == 400
    assert_error_response(response.json(), "UNSUPPORTED_FORMAT")


def test_upload_too_many_files_error_schema(test_client):
    """Error schema on /api/upload with >10 files."""
    files = [
        ("files", (f"test{i}.pdf", b"%PDF minimal", "application/pdf"))
        for i in range(11)
    ]
    response = test_client.post("/api/upload", files=files)
    assert response.status_code == 400
    assert_error_response(response.json(), "FILE_COUNT_EXCEEDED")


def test_upload_file_too_large_error_schema(test_client):
    """Error schema on /api/upload with file exceeding 10MB."""
    oversized_content = b"x" * (10 * 1024 * 1024 + 1)
    response = test_client.post(
        "/api/upload",
        files=[("files", ("big.pdf", oversized_content, "application/pdf"))],
    )
    assert response.status_code == 400
    assert_error_response(response.json(), "FILE_SIZE_EXCEEDED")


def test_chat_invalid_request_error_schema(test_client, sample_pdf_bytes):
    """Error schema on /api/chat with empty question."""
    # Upload first
    upload_resp = test_client.post(
        "/api/upload",
        files=[("files", ("test.pdf", sample_pdf_bytes, "application/pdf"))],
    )

    if upload_resp.status_code != 200:
        pytest.skip("Upload not available in test environment")

    session_id = upload_resp.json()["sessionId"]
    response = test_client.post(
        "/api/chat",
        json={"sessionId": session_id, "question": ""},
    )
    assert response.status_code == 400
    assert_error_response(response.json(), "INVALID_REQUEST")


def test_health_endpoint_returns_200(test_client):
    """GET /health should return 200 with status and version."""
    response = test_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_demo_endpoint_returns_200(test_client):
    """GET /api/demo should return 200 with required demo data structure."""
    response = test_client.get("/api/demo")
    assert response.status_code == 200
    body = response.json()

    # Validate structure
    assert "sessionId" in body
    assert "documents" in body
    assert "analysis" in body
    assert "preSeededMessages" in body

    # 5 documents
    assert len(body["documents"]) == 5

    # All docs have processingStatus completed
    for doc in body["documents"]:
        assert doc["processingStatus"] == "completed"

    # Required doc names
    doc_names = {d["filename"] for d in body["documents"]}
    assert "Supplier_A_Quotation.pdf" in doc_names
    assert "Supplier_B_Quotation.pdf" in doc_names
    assert "Existing_Contract_TechCorp.pdf" in doc_names
    assert "Invoice_TechCorp_March2026.pdf" in doc_names
    assert "Company_Procurement_Policy.pdf" in doc_names

    # At least 4 pre-seeded messages
    assert len(body["preSeededMessages"]) >= 4


def test_demo_analysis_meets_requirements(test_client):
    """Demo analysis data must meet spec requirements."""
    response = test_client.get("/api/demo")
    body = response.json()
    analysis = body["analysis"]

    # Risk requirements
    risks = analysis["risks"]
    high_risks = [r for r in risks if r["level"] == "HIGH"]
    medium_risks = [r for r in risks if r["level"] == "MEDIUM"]
    low_risks = [r for r in risks if r["level"] == "LOW"]

    assert len(high_risks) >= 2, "Demo needs at least 2 HIGH risks"
    assert len(medium_risks) >= 1, "Demo needs at least 1 MEDIUM risk"
    assert len(low_risks) >= 1, "Demo needs at least 1 LOW risk"

    # Comparison matrix
    matrix = analysis["comparisonMatrix"]
    assert len(matrix) >= 5, "Demo needs at least 5 comparison rows"

    supplier_b_wins = sum(
        1 for row in matrix if row.get("winner") == "Supplier B"
    )
    assert supplier_b_wins >= 3, "Supplier B must win at least 3 fields"

    # Conflicts
    assert len(analysis["conflicts"]) >= 2
    assert analysis["conflicts"][0]["severity"] == "HIGH"

    # Recommendation
    rec = analysis["recommendation"]
    assert "Supplier B" in rec["title"]
    assert abs(rec["confidence"] - 0.87) < 0.001
    assert len(rec["nextSteps"]) >= 4
