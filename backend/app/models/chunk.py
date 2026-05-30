from pydantic import BaseModel


class TranscriptChunk(BaseModel):
    chunk_id: str
    external_id: str
    text: str
