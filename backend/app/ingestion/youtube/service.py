from app.core.logging import get_logger
from app.ingestion.youtube.extractor import extract_youtube_metadata
from app.ingestion.youtube.parser import parse_youtube_video
from app.ingestion.youtube.transcript import get_youtube_transcript
from app.models.video import VideoData

logger = get_logger(__name__)


def ingest_youtube_video(
    url: str,
) -> VideoData:
    """
    Complete YouTube ingestion pipeline.

    Args:
        url: YouTube URL

    Returns:
        VideoData
    """

    logger.info(f"Starting YouTube ingestion: {url}")

    metadata = extract_youtube_metadata(url)
    transcript = get_youtube_transcript(url)

    video = parse_youtube_video(
        url=url,
        metadata=metadata,
        transcript=transcript,
    )

    logger.info(f"Completed ingestion: {video.title}")

    return video
