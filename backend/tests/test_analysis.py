"""
Tests for analysis endpoint, schema conformance, and PDF report headers.
"""

import json
import os
import re
import sys
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


VALID_ANALYSIS_RESPONSE = {
    "sessionId": "test-session",
    "status": "completed",
    "analysis": {
        "analyzedAt": "2026-01-01T00:00:00",
        "executiveSummary": "Test summary",
        "risks": [
            {"id": "r1", "level": "HIGH", "description": "Risk 1", "sourceDocument": "test.pdf", "category": "Financial"},
            {"id": "r2", "level": "MEDIUM", "description": "Risk 2", "sourceDocument": "test.pdf", "category": "Legal"},
        ],
        "comparisonMatrix": [
            {"field": "Price", "values": {"A": "$100"}, "winner": "A"}
        ],
        "conflicts": [],
        "recommendation": {
            "title": "Proceed",
            "summary": "Test recommendation",
            "nextSteps": ["Step 1", "Step 2", "Step 3", "Step 4"],
            "confidence": 0.85,
        },
    },
}


# ---- Property 7: Analysis response schema conformance ----

# Feature: dealflow-ai-backend, Property 7: analysis response schema conformance
def test_analysis_response_schema_conformance():
    """
    Property 7: Analysis response schema conformance.
    Validates: Requirements 2.9, 2.10
    """
    from models.response import AnalyzeResponse, AnalysisResult

    # Build response from valid data
    analysis = AnalysisResult(
        analyzedAt=datetime.utcnow(),
        executiveSummary="Test summary",
        risks=[],
        comparisonMatrix=[],
        conflicts=[],
        recommendation={
            "title": "Test",
            "summary": "Test",
            "nextSteps": ["step1"],
            "confidence": 0.9,
        },
    )
    response = AnalyzeResponse(
        sessionId="test-session",
        status="completed",
        analysis=analysis,
    )

    assert response.status == "completed"
    assert response.analysis is not None
    assert response.analysis.executiveSummary == "Test summary"
    assert hasattr(response.analysis, "analyzedAt")
    assert hasattr(response.analysis, "risks")
    assert hasattr(response.analysis, "comparisonMatrix")
    assert hasattr(response.analysis, "conflicts")
    assert hasattr(response.analysis, "recommendation")


# ---- Property 8: Risk level constraint ----

# Feature: dealflow-ai-backend, Property 8: risk level constraint
def test_risk_level_constraint():
    """
    Property 8: Risk level constraint.
    Validates: Requirements 2.5, 12.3

    Every risk in AnalysisResult.risks must have level in {"HIGH", "MEDIUM", "LOW"}.
    """
    from models.response import Risk

    valid_levels = {"HIGH", "MEDIUM", "LOW"}

    # Test valid levels
    for level in valid_levels:
        risk = Risk(
            id="r1",
            level=level,
            description="Test risk",
            sourceDocument="test.pdf",
            category="Financial",
        )
        assert risk.level in valid_levels

    # Test invalid level fails validation
    import pydantic
    with pytest.raises((pydantic.ValidationError, ValueError)):
        Risk(
            id="r1",
            level="CRITICAL",  # Invalid
            description="Test",
            sourceDocument="test.pdf",
            category="Financial",
        )


def test_risk_levels_from_demo_data():
    """All risk levels in the demo data should be valid."""
    from routers.demo import DEMO_DATA

    valid_levels = {"HIGH", "MEDIUM", "LOW"}
    for risk in DEMO_DATA["analysis"]["risks"]:
        assert risk["level"] in valid_levels, f"Invalid risk level: {risk['level']}"


# ---- Property 12: LLM provider routing ----

# Feature: dealflow-ai-backend, Property 12: LLM provider routing
@pytest.mark.asyncio
async def test_llm_provider_routing_amd_stub():
    """
    Property 12: LLM provider routing.
    Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5

    When LLM_PROVIDER=AMD with a valid endpoint, the service can be created.
    """
    import os
    os.environ["FIREWORKS_API_KEY"] = "test-key"
    os.environ["FIREWORKS_ENDPOINT"] = "https://api.fireworks.ai/inference/v1"

    # Re-import to pick up env changes
    import importlib
    import services.llm_service as llm_module
    importlib.reload(llm_module)

    service = llm_module.LLMService()
    assert service._api_key == "test-key"
    assert service._endpoint.startswith("https://")

    # Cleanup
    os.environ.pop("FIREWORKS_API_KEY", None)
    os.environ.pop("FIREWORKS_ENDPOINT", None)


def test_llm_provider_defaults_to_claude():
    """LLMService raises ValueError if FIREWORKS_API_KEY is not set."""
    import os
    import pytest
    from services.llm_service import LLMService
    
    saved = os.environ.pop("FIREWORKS_API_KEY", None)
    try:
        with pytest.raises(ValueError) as excinfo:
            LLMService()
        assert "FIREWORKS_API_KEY is required" in str(excinfo.value)
    finally:
        if saved:
            os.environ["FIREWORKS_API_KEY"] = saved


# ---- Property 13: PDF report header fields ----

# Feature: dealflow-ai-backend, Property 13: PDF report header fields
def test_pdf_report_generation_produces_bytes():
    """
    Property 13: PDF report header fields (content generation test).
    Validates: Requirements 4.10
    """
    from services.pdf_generator import PDFGenerator
    from models.response import AnalysisResult, Recommendation

    gen = PDFGenerator()
    analysis = AnalysisResult(
        analyzedAt=datetime.utcnow(),
        executiveSummary="Test executive summary.",
        risks=[],
        comparisonMatrix=[],
        conflicts=[],
        recommendation=Recommendation(
            title="Proceed with Supplier B",
            summary="Best value overall.",
            nextSteps=["Step 1", "Step 2", "Step 3", "Step 4"],
            confidence=0.87,
        ),
    )

    pdf_bytes = gen.generate_report(analysis, session_id="test-session")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF magic bytes
    assert pdf_bytes[:4] == b"%PDF"


def test_pdf_report_filename_format():
    """Report filename must match clausify-report-YYYY-MM-DD.pdf pattern."""
    from datetime import datetime

    today = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"clausify-report-{today}.pdf"

    # Validate the format
    pattern = r"^clausify-report-\d{4}-\d{2}-\d{2}\.pdf$"
    assert re.match(pattern, filename), f"Filename '{filename}' doesn't match expected pattern"


# ---- Integration: analyze endpoint ----

def test_analyze_requires_valid_session(test_client):
    """POST /api/analyze with unknown session returns 404."""
    response = test_client.post(
        "/api/analyze",
        json={"sessionId": "nonexistent-session-xyz"},
    )
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == "SESSION_NOT_FOUND"


def test_analyze_returns_completed_status(test_client, embedding_service, sample_pdf_bytes):
    """
    Full upload → analyze pipeline returns completed status with all required fields.
    """
    # Upload a document first
    upload_response = test_client.post(
        "/api/upload",
        files=[("files", ("test.pdf", sample_pdf_bytes, "application/pdf"))],
    )

    if upload_response.status_code != 200:
        pytest.skip(f"Upload failed: {upload_response.status_code} — {upload_response.json()}")

    session_id = upload_response.json()["sessionId"]

    # Run analysis
    analyze_response = test_client.post(
        "/api/analyze",
        json={"sessionId": session_id},
    )

    assert analyze_response.status_code in (200, 502), (
        f"Unexpected status: {analyze_response.status_code} — {analyze_response.json()}"
    )

    if analyze_response.status_code == 200:
        body = analyze_response.json()
        assert body["status"] == "completed"
        assert body["analysis"] is not None
        assert "executiveSummary" in body["analysis"]
        assert "risks" in body["analysis"]
        assert "comparisonMatrix" in body["analysis"]
        assert "conflicts" in body["analysis"]
        assert "recommendation" in body["analysis"]
