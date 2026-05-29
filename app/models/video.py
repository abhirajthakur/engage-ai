from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class VideoData(BaseModel):
    video_id: str  # A or B
    platform: str
    url: HttpUrl
    title: Optional[str] = None
    creator: Optional[str] = None
    creator_id: Optional[str] = None
    follower_count: Optional[int] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    engagement_rate: Optional[float] = None
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    hashtags: List[str] = []
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    transcript: str = ""
