from app.core.config import settings

from app.retrieval.vectorstores.base import VectorStore
from app.retrieval.vectorstores.chroma import ChromaVectorStore
from app.retrieval.vectorstores.qdrant import QdrantVectorStore

_vector_store = None


def get_vector_store() -> VectorStore:
    """
    Return configured vector store.
    """
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if settings.vector_db == "qdrant":
        _vector_store = QdrantVectorStore()

        return _vector_store

    _vector_store = ChromaVectorStore()

    return _vector_store
