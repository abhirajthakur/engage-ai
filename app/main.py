from fastapi import FastAPI

from app.core.logging import get_logger
from app.ingestion.youtube.extractor import extract_youtube_metadata

log = get_logger(__name__)

app = FastAPI(
    title="EngageAI",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


log.info("EngageAI API started")
