from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from app.cache.factory import get_cache
from app.cache.keys import transcript_cache_key
from app.core.logging import get_logger
from app.ingestion.youtube.utils import extract_shorts_video_id

logger = get_logger(__name__)


def get_youtube_transcript(
    url: str,
) -> str:
    """
    Fetch transcript if available.

    Returns empty string if unavailable.
    """

    video_id = extract_shorts_video_id(url)

    cache = get_cache()
    cache_key = transcript_cache_key(platform="youtube", external_id=video_id)

    cached = cache.get(cache_key)
    if cached is not None:
        logger.info(f"Transcript cache hit: {video_id}")

        return cached

    logger.info(f"Fetching transcript for {video_id}")

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        text = " ".join(chunk.text for chunk in transcript)
    except (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    ):
        logger.warning(f"No transcript available: {video_id}")
        text = ""

    cache.set(key=cache_key, value=text)

    return text
