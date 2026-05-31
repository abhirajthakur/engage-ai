from abc import ABC, abstractmethod

from app.models.retrieval import SearchResult


class VectorStore(ABC):
    """
    Abstract vector store interface.
    """

    @abstractmethod
    def add_documents(
        self,
        *,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        *,
        embedding: list[float],
        top_k: int,
        external_ids: list[str] | None = None,
    ) -> list[SearchResult]:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass
