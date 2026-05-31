from app.cache.base import CacheProvider


class RedisCacheProvider(CacheProvider):
    def get(
        self,
        key: str,
    ) -> str | None:
        raise NotImplementedError

    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        raise NotImplementedError

    def delete(
        self,
        key: str,
    ) -> None:
        raise NotImplementedError
