from pydantic import BaseModel

from fastapi import APIRouter

from app.ingestion.youtube.service import ingest_youtube_video

from app.ingestion.instagram.service import ingest_instagram_video

router = APIRouter()


class IngestRequest(BaseModel):
    youtube_url: str
    instagram_url: str


@router.post("/ingest")
def ingest_videos(
    request: IngestRequest,
):
    """
    Ingest YouTube and Instagram videos.
    """

    video_a = ingest_youtube_video(
        url=request.youtube_url,
        video_id="A",
    )

    video_b = ingest_instagram_video(
        url=request.instagram_url,
        video_id="B",
    )

    return {
        "video_a": (video_a.model_dump()),
        "video_b": (video_b.model_dump()),
    }
