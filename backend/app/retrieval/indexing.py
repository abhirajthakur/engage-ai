from app.models.video import VideoData
from app.retrieval.chunking import chunk_transcript
from app.retrieval.embeddings.bge import embed_texts
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

    if not chunks:
        return

    ids = [chunk.chunk_id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]

    embeddings = embed_texts(documents)

    metadatas = [
        {
            "chunk_id": chunk.chunk_id,
            "external_id": chunk.external_id,
            "platform": video.platform,
        }
        for chunk in chunks
    ]

    vector_store.add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
