import hashlib


def metadata_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    """
    Metadata cache key.
    """

    return f"{platform}:metadata:{external_id}"


def transcript_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    """
    Transcript cache key.
    """

    return f"{platform}:transcript:{external_id}"


def embedding_key(text: str) -> str:
    """
    Embedding cache key.
    """

    digest = hashlib.sha256(
        text.encode(
            "utf-8",
        ),
    ).hexdigest()

    return f"embedding:{digest}"


def session_cache_key(
    session_id: str,
) -> str:
    return f"session:{session_id}"


def conversation_cache_key(
    session_id: str,
) -> str:
    return f"conversation:{session_id}"
