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

    searchable_text = "\n\n".join(
        [
            f"Title: {video.title}",
            f"Description: {video.description}",
            f"Creator: {video.creator}",
            f"Views: {video.views}",
            f"Likes: {video.likes}",
            f"Comments: {video.comments}",
            "",
            video.transcript,
        ]
    )

    chunks = chunk_transcript(
        transcript=searchable_text,
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
            "title": video.title,
            "creator": video.creator,
        }
        for chunk in chunks
    ]

    vector_store.add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
