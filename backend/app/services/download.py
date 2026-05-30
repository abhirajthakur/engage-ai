from pathlib import Path

import httpx

from app.core.logging import get_logger

logger = get_logger(__name__)


async def download_file(
    *,
    url: str,
    output_path: str,
) -> str:
    """
    Download remote file.

    Args:
        url: File URL
        output_path: Destination path

    Returns:
        Local path
    """

    logger.info(f"Downloading file from {url}")

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
        )
        response.raise_for_status()

    Path(output_path).write_bytes(response.content)

    return output_path
