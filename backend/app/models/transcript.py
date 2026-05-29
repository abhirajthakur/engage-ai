from pydantic import BaseModel


class TranscriptData(BaseModel):
    language: str
    is_generated: bool
    text: str
