from typing import Any

import yt_dlp

from app.core.logging import get_logger

logger = get_logger(__name__)


def extract_youtube_metadata(
    url: str,
) -> dict[str, Any]:
    logger.info(f"Extracting metadata: {url}")

    with yt_dlp.YoutubeDL(
        {
            "quiet": True,
            "skip_download": True,
        }
    ) as ydl:
        info = ydl.extract_info(
            url,
            download=False,
        )

    logger.info(f"Metadata extracted: {info.get('title')}")

    return info
