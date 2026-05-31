from app.cache.base import CacheProvider
from app.cache.diskcache import DiskCacheProvider


def get_cache() -> CacheProvider:

    return DiskCacheProvider()
