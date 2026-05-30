from typing import Any

from pydantic import HttpUrl

from app.models.video import VideoData
from app.services.engagement import calculate_engagement_rate


def parse_instagram_video(
    *,
    url: str,
    metadata: dict[str, Any],
    transcript: str,
) -> VideoData:
    """
    Convert raw Instagram data
    into VideoData.
    """

    views = metadata.get("videoViewCount")

    likes = metadata.get("likesCount")

    if likes == -1:
        likes = None

    comments = metadata.get("commentsCount")

    return VideoData(
        external_id=str(metadata.get("id")),
        platform="instagram",
        url=HttpUrl(url),
        title=metadata.get("caption"),
        creator=metadata.get("ownerUsername"),
        creator_id=metadata.get("ownerId"),
        follower_count=None,
        views=views,
        likes=likes,
        comments=comments,
        duration=int(
            metadata.get(
                "videoDuration",
                0,
            )
        ),
        upload_date=metadata.get("timestamp"),
        hashtags=metadata.get(
            "hashtags",
            [],
        ),
        description=metadata.get("caption"),
        thumbnail_url=metadata.get("displayUrl"),
        transcript=transcript,
        engagement_rate=calculate_engagement_rate(
            likes=likes,
            comments=comments,
            views=views,
        ),
    )
