from pydantic import BaseModel

from app.models.video import VideoData


class ComparisonSession(BaseModel):
    session_id: str
    video_a: VideoData
    video_b: VideoData
