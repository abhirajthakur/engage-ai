from app.chunking.splitter import chunk_transcript
from app.models.video import VideoData
from app.retrieval.embeddings.bge import embed_text
from app.retrieval.vectorstores.factory import get_vector_store


def index_video(
    video: VideoData,
) -> None:
    """
    Index a video's transcript.

    Args:
        video: VideoData
    """

    vector_store = get_vector_store()

    chunks = chunk_transcript(
        transcript=video.transcript,
        external_id=video.external_id,
    )

    ids: list[str] = []
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict] = []

    for chunk in chunks:
        ids.append(chunk.chunk_id)
        documents.append(chunk.text)
        embeddings.append(embed_text(chunk.text))
        metadatas.append(
            {
                "chunk_id": chunk.chunk_id,
                "external_id": chunk.external_id,
                "platform": video.platform
            }
        )

    vector_store.add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
