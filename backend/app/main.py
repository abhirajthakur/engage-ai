from fastapi import FastAPI

from app.api.ingest import router as ingest_router
from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)

app = FastAPI(
    title="EngageAI",
)
log.info("EngageAI API started")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(ingest_router, prefix=settings.api_prefix)
