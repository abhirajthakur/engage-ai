def transcript_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    return f"transcript:{platform}:{external_id}"


def metadata_key(
    *,
    platform: str,
    external_id: str,
) -> str:
    return f"metadata:{platform}:{external_id}"
