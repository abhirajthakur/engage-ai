from urllib.parse import urlparse


def extract_reel_id(
    url: str,
) -> str:
    """
    Extract Instagram reel id from URL.

    Examples:

    https://www.instagram.com/reel/C8abc123/
    -> C8abc123

    https://instagram.com/reel/C8abc123
    -> C8abc123
    """

    path_parts = [
        part
        for part in urlparse(
            url,
        ).path.split(
            "/",
        )
        if part
    ]

    if len(path_parts) >= 2 and path_parts[0] == "reel":
        return path_parts[1]

    raise ValueError(f"Invalid Instagram reel URL: {url}")
