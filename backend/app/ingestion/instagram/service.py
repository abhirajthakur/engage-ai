from app.core.logging import get_logger
from app.ingestion.instagram.extractor import extract_instagram_metadata
from app.ingestion.instagram.parser import parse_instagram_video
from app.models.video import VideoData
from app.services.download import download_file
from app.services.transcription import transcribe_audio

logger = get_logger(__name__)


def ingest_instagram_reel(
    url: str,
    video_id: str,
) -> VideoData:
    """
    Complete Instagram ingestion pipeline.

    Args:
        url: Reel URL
        video_id: A or B

    Returns:
        VideoData
    """

    logger.info(f"Starting Instagram ingestion: {url}")

    metadata = extract_instagram_metadata(url)
    audio_url = metadata.get("audioUrl")
    transcript = ""

    if audio_url:
        audio_path = download_file(
            url=audio_url,
            output_path=(f"temp/{video_id}_audio.mp4"),
        )
        transcript = transcribe_audio(audio_path)

    video = parse_instagram_video(
        url=url,
        metadata=metadata,
        transcript=transcript,
        video_id=video_id,
    )

    logger.info(f"Completed Instagram ingestion: {video.creator}")

    return video
