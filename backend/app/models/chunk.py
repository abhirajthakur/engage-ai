from pydantic import BaseModel


class TranscriptChunk(BaseModel):
    chunk_id: str
    video_id: str
    text: str
