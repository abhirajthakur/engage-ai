from uuid import uuid4

from qdrant_client import QdrantClient

from qdrant_client.models import Distance
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams

from app.models.retrieval import SearchResult
from app.retrieval.vectorstores.base import VectorStore


class QdrantVectorStore(VectorStore):
    COLLECTION_NAME = "transcripts"
    VECTOR_SIZE = 384

    def __init__(self) -> None:
        self.client = QdrantClient(path="storage/qdrant")
        self._ensure_collection()

    def _ensure_collection(
        self,
    ) -> None:
        collections = self.client.get_collections()
        exists = any(
            collection.name == self.COLLECTION_NAME
            for collection in collections.collections
        )

        if exists:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    def add_documents(
        self,
        *,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        points: list[PointStruct] = []

        for idx, chunk_id in enumerate(ids):
            payload = {
                "chunk_id": chunk_id,
                "document": documents[idx],
                **metadatas[idx],
            }

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embeddings[idx],
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        *,
        embedding: list[float],
        top_k: int,
    ) -> list[SearchResult]:
        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=embedding,
            limit=top_k,
        )

        search_results: list[SearchResult] = []

        for point in response.points:
            payload = point.payload or {}

            search_results.append(
                SearchResult(
                    chunk_id=str(
                        payload.get(
                            "chunk_id",
                            "",
                        )
                    ),
                    video_id=str(
                        payload.get(
                            "video_id",
                            "",
                        )
                    ),
                    text=str(
                        payload.get(
                            "document",
                            "",
                        )
                    ),
                    score=float(point.score),
                )
            )

        return search_results

    def delete_all(
        self,
    ) -> None:
        self.client.delete_collection(collection_name=self.COLLECTION_NAME)
        self._ensure_collection()
