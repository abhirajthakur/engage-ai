from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # e.g., "user", "assistant"
    content: str
