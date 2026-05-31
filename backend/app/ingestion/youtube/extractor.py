import json
from typing import Any

import yt_dlp

from app.cache.factory import get_cache
from app.cache.keys import metadata_key
from app.core.logging import get_logger
from app.ingestion.youtube.utils import extract_shorts_video_id

logger = get_logger(__name__)


def extract_youtube_metadata(
    url: str,
) -> dict[str, Any]:
    logger.info(f"Extracting metadata: {url}")

    video_id = extract_shorts_video_id(url)

    cache = get_cache()
    key = metadata_key(
        platform="youtube",
        external_id=video_id,
    )

    cached = cache.get(
        key,
    )

    if cached is not None:
        logger.info(f"Metadata cache hit: {video_id}")
        return json.loads(cached)

    with yt_dlp.YoutubeDL(
        {
            "quiet": True,
            "skip_download": True,
            "js_runtimes": {"node": {}},
            "remote_components": ["ejs:github"],
        }
    ) as ydl:
        metadata = ydl.extract_info(
            url,
            download=False,
        )

    cache.set(key, json.dumps(metadata))

    logger.info(f"Metadata extracted: {metadata.get('title')}")

    return metadata
