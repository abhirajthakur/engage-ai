import json
from app.cache.factory import get_cache
from app.cache.keys import metadata_key
from app.ingestion.instagram.utils import extract_reel_id
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

    cache = get_cache()

    reel_id = extract_reel_id(url)
    cache_key = metadata_key(platform="instagram", external_id=reel_id)

    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("Instagram metadata cache hit")
        return json.loads(cached)

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

    metadata = dataset_items[0]

    cache.set(cache_key, json.dumps(metadata))

    return metadata
