from typing import Any, cast

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.logging import get_logger
from app.models.retrieval import SearchResult
from app.retrieval.vectorstores.base import VectorStore

logger = get_logger(__name__)


class ChromaVectorStore(VectorStore):
    """
    Chroma implementation.
    """

    def __init__(
        self,
        collection_name: str = "transcripts",
    ) -> None:
        self.client = chromadb.PersistentClient(path="storage/chroma")
        self.collection: Collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        *,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=cast(Any, embeddings),
            metadatas=cast(Any, metadatas),
        )

    def search(
        self,
        *,
        embedding: list[float],
        top_k: int,
        external_ids: list[str] | None = None,
    ) -> list[SearchResult]:
        query_kwargs: dict = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }

        if external_ids:
            if len(external_ids) == 1:
                query_kwargs["where"] = {
                    "external_id": external_ids[0],
                }
            else:
                query_kwargs["where"] = {
                    "$or": [
                        {
                            "external_id": external_id,
                        }
                        for external_id in external_ids
                    ]
                }

        results = self.collection.query(
            **query_kwargs,
        )

        documents_nested = results.get("documents")
        metadatas_nested = results.get("metadatas")
        distances_nested = results.get("distances")

        if not documents_nested or not metadatas_nested:
            return []

        documents = documents_nested[0]
        metadatas = metadatas_nested[0]
        distances = distances_nested[0] if distances_nested else []

        search_results: list[SearchResult] = []

        for idx, document in enumerate(documents):
            metadata = metadatas[idx] if idx < len(metadatas) else {}
            metadata = metadata or {}

            search_results.append(
                SearchResult(
                    chunk_id=str(metadata.get("chunk_id", "")),
                    external_id=str(metadata.get("external_id", "")),
                    text=document,
                    score=(float(distances[idx]) if idx < len(distances) else 0.0),
                )
            )

        return search_results

    def delete_all(self) -> None:
        ids = self.collection.get()["ids"]
        if ids:
            self.collection.delete(ids=ids)
