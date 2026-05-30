from pydantic import BaseModel


class SearchResult(BaseModel):
    """
    Normalized retrieval result.

    This model is returned by all vector stores
    regardless of implementation.
    """
    chunk_id: str
    external_id: str
    text: str
    score: float
    source: str | None = None
