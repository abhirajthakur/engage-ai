from dataclasses import dataclass, field

from app.models.message import ChatMessage
from app.models.retrieval import SearchResult
from app.models.video import VideoData


@dataclass
class GraphState:
    session_id: str
    query: str
    video_a: VideoData | None = None
    video_b: VideoData | None = None
    messages: list[ChatMessage] = field(default_factory=list)
    retrieved_chunks: list[SearchResult] = field(default_factory=list)
    prompt: str = ""
