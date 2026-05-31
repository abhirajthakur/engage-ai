import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ingestion.instagram.service import ingest_instagram_reel
from app.ingestion.youtube.service import ingest_youtube_short

router = APIRouter()


class IngestRequest(BaseModel):
    youtube_url: str
    instagram_url: str


def validate_youtube_short(
    url: str,
) -> bool:
    return "youtube.com/shorts/" in url


@router.post("/ingest")
async def ingest_videos(request: IngestRequest):
    """
    Ingest YouTube and Instagram videos.
    """

    if not validate_youtube_short(request.youtube_url):
        raise HTTPException(
            status_code=400, detail="Please provide a YouTube Shorts URL"
        )

    video_a, video_b = await asyncio.gather(
        ingest_youtube_short(url=request.youtube_url),
        ingest_instagram_reel(url=request.instagram_url),
    )

    return {
        "video_a": video_a.model_dump(),
        "video_b": video_b.model_dump(),
    }
