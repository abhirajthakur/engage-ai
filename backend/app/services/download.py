from pathlib import Path

import httpx

from app.core.logging import get_logger

logger = get_logger(__name__)


def download_file(
    url: str,
    output_path: str,
) -> str:
    """
    Download remote file
    """

    logger.info(f"Downloading file from {url}")

    response = httpx.get(
        url,
        timeout=120,
        follow_redirects=True,
    )

    response.raise_for_status()

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(output_path).write_bytes(response.content)

    logger.info(f"Saved file to {output_path}")

    return output_path
