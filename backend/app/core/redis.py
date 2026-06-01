from redis import Redis

from app.core.config import settings

_client: Redis | None = None


def get_redis() -> Redis:
    global _client

    if _client is None:
        _client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=0,
            decode_responses=True,
        )

    return _client
