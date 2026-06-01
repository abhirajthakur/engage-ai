from pydantic import BaseModel


class SourceCitation(BaseModel):
    external_id: str
    chunk_id: str
    text: str


class ChatResult(BaseModel):
    answer: str
    sources: list[SourceCitation]
