from typing import Any

from apify_client import ApifyClient

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def extract_instagram_metadata(
    url: str,
) -> dict[str, Any]:
    """
    Extract Instagram Reel metadata.
    """

    logger.info(f"Extracting Instagram data: {url}")

    client = ApifyClient(settings.apify_api_token)
    actor = client.actor("apify/instagram-scraper")

    run_input = {
        "directUrls": [url],
        "resultsLimit": 1,
    }

    run = actor.call(run_input=run_input)

    if not run:
        raise ValueError("Apify run returned None")

    dataset_id = run.default_dataset_id
    dataset_items = list(client.dataset(dataset_id).iterate_items())

    if not dataset_items:
        raise ValueError("No Instagram data returned")

    return dataset_items[0]
