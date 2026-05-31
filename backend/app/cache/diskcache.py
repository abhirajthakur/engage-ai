from diskcache import Cache

from app.cache.base import CacheProvider


class DiskCacheProvider(CacheProvider):
    def __init__(
        self,
    ) -> None:
        self.cache = Cache(
            "storage/cache",
        )

    def get(
        self,
        key: str,
    ) -> str | None:
        return self.cache.get(key)

    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        self.cache.set(
            key,
            value,
            expire=ttl_seconds,
        )

    def delete(
        self,
        key: str,
    ) -> None:
        self.cache.pop(key)
