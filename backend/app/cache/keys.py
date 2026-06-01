import hashlib


def metadata_cache_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    return f"{platform.lower()}:metadata:{external_id}"


def transcript_cache_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    return f"{platform.lower()}:transcript:{external_id}"


def embedding_cache_key(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return f"embedding:{digest}"


def session_cache_key(session_id: str) -> str:
    return f"session:{session_id}"


def conversation_cache_key(session_id: str) -> str:
    return f"conversation:{session_id}"
