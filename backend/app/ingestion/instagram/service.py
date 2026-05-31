from app.cache.keys import transcript_key
from app.cache.factory import get_cache
import asyncio

from app.core.logging import get_logger
from app.ingestion.instagram.extractor import extract_instagram_metadata
from app.ingestion.instagram.parser import parse_instagram_video
from app.models.video import VideoData
from app.services.download import download_file
from app.services.transcription import transcribe_audio

logger = get_logger(__name__)


async def ingest_instagram_video(
    url: str,
) -> VideoData:
    """
    Complete Instagram Reel ingestion pipeline.

    Args:
        url: Reel URL

    Returns:
        VideoData
    """

    logger.info(f"Starting Instagram ingestion: {url}")

    metadata = await asyncio.to_thread(
        extract_instagram_metadata,
        url,
    )

    transcript = ""

    audio_url = metadata.get("audioUrl")
    external_id = str(metadata.get("id", "unknown"))

    cache = get_cache()

    transcript_cache_key = transcript_key(
        platform="instagram",
        external_id=external_id,
    )

    cached_transcript = cache.get(transcript_cache_key)

    if cached_transcript is not None:
        logger.info(f"Instagram transcript cache hit: {external_id}")
        transcript = cached_transcript
    elif audio_url:
        audio_path = await download_file(
            url=audio_url,
            output_path=(f"storage/audio/instagram/{external_id}.mp4"),
        )

        transcript = await asyncio.to_thread(
            transcribe_audio,
            audio_path,
        )

        cache.set(transcript_cache_key, transcript)

    video = parse_instagram_video(
        url=url,
        metadata=metadata,
        transcript=transcript,
    )

    logger.info(f"Completed Instagram ingestion: {video.creator}")

    return video
