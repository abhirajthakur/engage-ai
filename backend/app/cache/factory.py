from app.cache.base import CacheProvider
from app.cache.diskcache import DiskCacheProvider
from app.cache.redis import RedisCacheProvider
from app.core.config import settings

_cache: CacheProvider | None = None


def get_cache() -> CacheProvider:
    global _cache

    if _cache is None:
        if settings.environment == "production":
            _cache = RedisCacheProvider()
        else:
            _cache = DiskCacheProvider()

    return _cache
