from urllib.parse import urlparse


def extract_shorts_video_id(url: str) -> str:
    """
    Extract YouTube video ID from Shorts URLs.
    """
    parsed = urlparse(url)

    if parsed.netloc not in {"youtube.com", "www.youtube.com"}:
        raise ValueError("Invalid YouTube Shorts URL")

    parts = parsed.path.strip("/").split("/")

    if len(parts) != 2 or parts[0] != "shorts":
        raise ValueError("Invalid YouTube Shorts URL")

    return parts[1]
