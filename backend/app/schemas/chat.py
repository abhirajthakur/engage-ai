from typing import Literal

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


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    content: str


class SourcesEvent(BaseModel):
    type: Literal["sources"] = "sources"
    sources: list[SourceCitationSchema]


class DoneEvent(BaseModel):
    type: Literal["done"] = "done"


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str
