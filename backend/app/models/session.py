from pydantic import BaseModel


class ComparisonSession(BaseModel):
    session_id: str
    video_a_external_id: str
    video_b_external_id: str
