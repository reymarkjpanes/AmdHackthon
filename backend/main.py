"""
Clausify AI Backend — FastAPI Application
AMD MI300X-powered document intelligence service.
"""

import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---- Import routers ----
from routers import upload, analyze, chat, report, demo

# ---- Rate Limiter ----
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# ---- Create FastAPI app ----
app = FastAPI(
    title="Clausify AI",
    version="1.0.0",
    description="AMD MI300X-powered enterprise procurement document intelligence API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---- CORS Middleware ----
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
else:
    allowed_origins = ["*"]

app.state.limiter = limiter

async def _custom_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests. Please wait a moment before trying again.",
            "code": "RATE_LIMITED",
            "details": {"retry_after": str(exc.retry_after)},
        },
    )

app.add_exception_handler(RateLimitExceeded, _custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
)

# ---- Register Routers ----
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(report.router, prefix="/api", tags=["report"])
app.include_router(demo.router, prefix="/api", tags=["demo"])


# ---- Global Exception Handler ----
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all exception handler.
    Logs the full traceback server-side but never exposes it in the response.
    """
    logger.exception(f"Unhandled exception for {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred.",
            "code": "UNKNOWN_ERROR",
            "details": None,
        },
    )


# ---- Health Check ----
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


# ---- Startup Event ----
@app.on_event("startup")
async def startup_event():
    """
    Initialize all services at startup and inject into router modules.
    """
    logger.info("Clausify AI Backend starting up...")
    logger.info("AMD MI300X-powered document intelligence")

    try:
        from services.document_parser import DocumentParser
        from services.embedding_service import EmbeddingService
        from services.vector_store import VectorStore
        from services.session_manager import SessionManager
        from services.llm_service import LLMService, ConfigurationError
        from services.conflict_engine import ConflictEngine
        from services.analysis_service import AnalysisService
        from services.pdf_generator import PDFGenerator

        document_parser = DocumentParser()
        logger.info("DocumentParser initialized")

        embedding_service = EmbeddingService()
        logger.info("EmbeddingService initialized (all-MiniLM-L6-v2)")

        # Warm the embedding model
        try:
            _ = embedding_service.embed("warmup clausify ai amd mi300x")
            logger.info("Embedding model warmed up")
        except Exception as warm_err:
            logger.warning(f"Warmup failed (non-fatal): {warm_err}")

        vector_store = VectorStore()
        logger.info("VectorStore initialized (ChromaDB in-memory)")

        session_manager = SessionManager()
        logger.info("SessionManager initialized")

        try:
            llm_service = LLMService()
            logger.info(f"LLMService initialized (provider: {llm_service.provider.value})")
        except ConfigurationError as e:
            logger.error(f"LLMService configuration error: {e}")
            logger.warning("Set ANTHROPIC_API_KEY or use LLM_PROVIDER=AMD for mock mode")
            llm_service = _create_stub_llm_service()

        conflict_engine = ConflictEngine(llm_service)
        logger.info("ConflictEngine initialized")

        analysis_service = AnalysisService(llm_service, conflict_engine, session_manager)
        logger.info("AnalysisService initialized")

        pdf_generator = PDFGenerator()
        logger.info("PDFGenerator initialized")

        # --- Inject services into routers ---
        upload._document_parser = document_parser
        upload._embedding_service = embedding_service
        upload._vector_store = vector_store
        upload._session_manager = session_manager

        analyze._analysis_service = analysis_service
        analyze._session_manager = session_manager
        analyze._vector_store = vector_store

        chat._embedding_service = embedding_service
        chat._vector_store = vector_store
        chat._session_manager = session_manager
        chat._llm_service = llm_service

        report._pdf_generator = pdf_generator
        report._session_manager = session_manager

        logger.info("All services initialized — Clausify AI is ready!")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        logger.exception("Startup exception details:")


def _create_stub_llm_service():
    """Create a stub LLM service for when configuration is missing."""
    from services.llm_service import LLMService, LLMProvider

    class StubLLMService(LLMService):
        def __init__(self):
            self.provider = LLMProvider.AMD
            self._amd_endpoint = ""
            self._amd_api_key = ""
            logger.warning("Running with STUB LLM service")

    return StubLLMService()


# ---- Entry Point ----
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
