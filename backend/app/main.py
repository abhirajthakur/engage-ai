from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("EngageAI backend starting up")

    yield

    logger.info("EngageAI backend shutting down")


app = FastAPI(
    title="EngageAI",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(ingest_router, prefix=settings.api_prefix)
app.include_router(chat_router, prefix=settings.api_prefix)
