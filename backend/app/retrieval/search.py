from app.models.retrieval import SearchResult
from app.retrieval.embeddings.bge import embed_text
from app.retrieval.vectorstores.factory import get_vector_store


def search_chunks(
    query: str,
    external_ids: list[str] | None = None,
    top_k: int = 5,
) -> list[SearchResult]:
    """
    Search transcript chunks.

    Args:
        query: User query
        external_ids: Optional list of external IDs to filter the search
        top_k: Number of results

    Returns:
        list[SearchResult]
    """

    vector_store = get_vector_store()
    query_embedding = embed_text(query)

    return vector_store.search(
        embedding=query_embedding,
        top_k=top_k,
        external_ids=external_ids,
    )
