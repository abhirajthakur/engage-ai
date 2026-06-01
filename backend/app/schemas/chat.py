from pydantic import BaseModel


class SourceCitationSchema(BaseModel):
    external_id: str
    chunk_id: str
    text: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCitationSchema]
