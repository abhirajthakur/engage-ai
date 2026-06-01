import asyncio

from fastapi import APIRouter, HTTPException

from app.ingestion.instagram.service import ingest_instagram_reel
from app.ingestion.youtube.service import ingest_youtube_short
from app.retrieval.indexing import index_video
from app.schemas.ingest import IngestRequest, IngestResponse
from app.session.service import create_session

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_videos(request: IngestRequest):
    """
    Ingest one YouTube Short and one Instagram Reel concurrently.
    """
    try:
        video_a, video_b = await asyncio.gather(
            ingest_youtube_short(url=request.youtube_url),
            ingest_instagram_reel(url=request.instagram_url),
        )

        await asyncio.gather(
            asyncio.to_thread(index_video, video_a),
            asyncio.to_thread(index_video, video_b),
        )

        session = create_session(
            video_a=video_a,
            video_b=video_b,
        )

        return IngestResponse(
            session_id=session.session_id,
            video_a=video_a,
            video_b=video_b,
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
