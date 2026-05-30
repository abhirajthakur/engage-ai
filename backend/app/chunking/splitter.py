from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import TranscriptChunk


def chunk_transcript(
    transcript: str,
    video_id: str,
) -> list[TranscriptChunk]:
    """
    Split transcript into chunks.

    Args:
        transcript: Full transcript
        video_id: A or B

    Returns:
        list[TranscriptChunk]
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    chunks = splitter.split_text(transcript)

    return [
        TranscriptChunk(
            chunk_id=f"{video_id}_{idx}",
            video_id=video_id,
            text=text,
        )
        for idx, text in enumerate(chunks)
    ]
