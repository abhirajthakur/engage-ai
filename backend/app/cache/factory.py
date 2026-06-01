from app.cache.base import CacheProvider
from app.cache.diskcache import DiskCacheProvider
from app.cache.redis import RedisCacheProvider
from app.core.config import settings

_cache: CacheProvider | None = None


def get_cache() -> CacheProvider:
    global _cache

    if _cache is None:
        if settings.cache_provider == "redis":
            _cache = RedisCacheProvider()
        elif settings.cache_provider == "disk":
            _cache = DiskCacheProvider()
        else:
            raise ValueError(f"Unsupported cache provider: {settings.cache_provider}")

    return _cache
