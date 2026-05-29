import re

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from app.core.logging import get_logger

logger = get_logger(__name__)


def extract_video_id(
    url: str,
) -> str:
    """
    Extract YouTube video ID from URL.
    """
    match = re.search(
        r"v=([^&]+)",
        url,
    )
    if not match:
        raise ValueError("Invalid YouTube URL")

    return match.group(1)


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
    video_id = extract_video_id(url)

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

    logger.info(f"Transcript fetched successfully for {video_id}")

    return transcript_text
