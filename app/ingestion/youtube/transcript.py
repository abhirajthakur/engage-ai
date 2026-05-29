import re

from youtube_transcript_api import YouTubeTranscriptApi

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
    """
    video_id = extract_video_id(url)

    logger.info(f"Fetching transcript for {video_id}")

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        transcript_text = " ".join(snippet.text for snippet in transcript)

        logger.info(f"Transcript fetched successfully for {video_id}")

        return transcript_text

    except Exception as e:
        logger.exception("Failed to fetch transcript")
        raise e
