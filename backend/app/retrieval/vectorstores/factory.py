from app.core.config import settings
from app.retrieval.vectorstores.base import VectorStore
from app.retrieval.vectorstores.chroma import ChromaVectorStore
from app.retrieval.vectorstores.qdrant import QdrantVectorStore

_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if settings.vector_db == "qdrant":
        _vector_store = QdrantVectorStore()
    elif settings.vector_db == "chroma":
        _vector_store = ChromaVectorStore()
    else:
        raise ValueError(f"Unsupported vector_db: {settings.vector_db}")

    return _vector_store
