from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from app.cache.factory import get_cache
from app.cache.keys import transcript_key
from app.core.logging import get_logger
from app.ingestion.youtube.utils import extract_shorts_video_id

logger = get_logger(__name__)


def get_youtube_transcript(
    url: str,
) -> str:
    """
    Fetch transcript from YouTube.

    Strategy:
    1. Try English transcript
    2. Fall back to first available transcript
    3. Raise only if none exist
    """
    video_id = extract_shorts_video_id(url)

    cache = get_cache()

    key = transcript_key(
        platform="youtube",
        external_id=video_id,
    )

    cached = cache.get(key)

    if cached is not None:
        logger.info(f"Transcript cache hit: {video_id}")
        return cached

    logger.info(f"Fetching transcript for {video_id}")

    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(
            video_id,
            languages=["en"],
        )
    except NoTranscriptFound:
        logger.warning("English transcript not found. Trying available transcripts.")

        transcript_list = api.list(video_id)
        available = list(transcript_list)
        if not available:
            raise ValueError(f"No transcripts available for {video_id}")

        transcript = available[0].fetch()

    transcript_text = " ".join(snippet.text for snippet in transcript)

    cache.set(key, transcript_text)

    logger.info(f"Transcript fetched successfully for {video_id}")

    return transcript_text
