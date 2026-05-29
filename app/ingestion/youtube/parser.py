from pydantic import HttpUrl

from app.models.video import VideoData


def parse_youtube_data(
    url: str,
    metadata: dict,
    transcript: str,
    video_id: str,
) -> VideoData:
    views = metadata.get("view_count") or 0
    likes = metadata.get("like_count") or 0
    comments = metadata.get("comment_count") or 0
    engagement_rate = ((likes + comments) / views) * 100 if views > 0 else 0

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
        engagement_rate=round(
            engagement_rate,
            2,
        ),
    )
