from app.cache.base import CacheProvider
from app.core.redis import get_redis


class RedisCacheProvider(CacheProvider):
    def __init__(self):
        self.client = get_redis()

    def get(
        self,
        key: str,
    ) -> str | None:
        value = self.client.get(key)

        return str(value) if value is not None else None

    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        self.client.set(key, value, ex=ttl_seconds)

    def delete(
        self,
        key: str,
    ) -> None:
        self.client.delete(key)
