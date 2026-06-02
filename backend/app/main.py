from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router
from app.core.config import settings
from app.core.logging import get_logger
from app.retrieval.embeddings.bge import get_embedding_model
from app.services.transcription import get_whisper_model

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting EngageAI application")

    try:
        start = perf_counter()

        logger.info("Loading embedding model...")
        get_embedding_model()
        logger.info(
            "Embedding model loaded successfully",
            extra={"startup_step": "embeddings"},
        )

        logger.info("Loading Whisper model...")
        get_whisper_model()
        logger.info(
            "Whisper model loaded successfully",
            extra={"startup_step": "whisper"},
        )

        elapsed = perf_counter() - start
        logger.info(
            "Application startup completed",
            extra={"startup_time_seconds": round(elapsed, 2)},
        )

        yield

    except Exception:
        logger.exception("Application startup failed")
        raise

    finally:
        logger.info("Shutting down EngageAI application")


app = FastAPI(title="EngageAI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(ingest_router, prefix=settings.api_prefix)
app.include_router(chat_router, prefix=settings.api_prefix)
