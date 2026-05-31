from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import TranscriptChunk


def chunk_transcript(
    transcript: str,
    external_id: str,
) -> list[TranscriptChunk]:
    """
    Split transcript into chunks.

    Args:
        transcript: Full transcript

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
            chunk_id=f"{external_id}_{idx}",
            external_id=external_id,
            text=text,
        )
        for idx, text in enumerate(chunks)
    ]
