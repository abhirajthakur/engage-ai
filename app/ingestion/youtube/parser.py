from typing import Any

from pydantic import HttpUrl

from app.models.video import VideoData
from app.services.engagement import (
    calculate_engagement_rate,
)


def parse_youtube_video(
    *,
    url: str,
    metadata: dict[str, Any],
    transcript: str,
    video_id: str,
) -> VideoData:
    """
    Convert raw yt-dlp metadata
    into normalized VideoData.

    Returns:
        VideoData
    """

    views = metadata.get("view_count")
    likes = metadata.get("like_count")
    comments = metadata.get("comment_count")

    return VideoData(
        video_id=video_id,
        platform="youtube",
        url=HttpUrl(url),
        title=metadata.get("title"),
        creator=metadata.get("channel"),
        creator_id=metadata.get("channel_id"),
        follower_count=metadata.get("channel_follower_count"),
        views=views,
        likes=likes,
        comments=comments,
        duration=metadata.get("duration"),
        upload_date=metadata.get("upload_date"),
        hashtags=metadata.get("tags", []),
        description=metadata.get("description"),
        thumbnail_url=metadata.get("thumbnail"),
        transcript=transcript,
        engagement_rate=calculate_engagement_rate(
            likes=likes,
            comments=comments,
            views=views,
        ),
    )
