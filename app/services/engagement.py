from typing import Optional


def calculate_engagement_rate(
    likes: Optional[int],
    comments: Optional[int],
    views: Optional[int],
) -> float:
    """
    Calculate engagement rate.

    Formula:
    (likes + comments) / views * 100
    """

    if not views:
        return 0.0

    likes = likes or 0
    comments = comments or 0

    return round(
        ((likes + comments) / views) * 100,
        2,
    )
