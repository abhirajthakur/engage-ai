from app.cache.factory import get_cache
from app.cache.keys import session_cache_key
from app.core.config import settings
from app.models.session import ComparisonSession


def save_session(session: ComparisonSession) -> None:
    """
    Persist session.
    """

    cache = get_cache()

    cache.set(
        key=session_cache_key(session.session_id),
        value=session.model_dump_json(),
        ttl_seconds=settings.session_ttl_seconds,
    )


def get_session(session_id: str) -> ComparisonSession | None:
    """
    Load session.
    """

    cache = get_cache()
    data = cache.get(session_cache_key(session_id))

    if data is None:
        return None

    return ComparisonSession.model_validate_json(data)


def delete_session(session_id: str) -> None:
    """
    Delete session.
    """

    cache = get_cache()
    cache.delete(session_cache_key(session_id))
