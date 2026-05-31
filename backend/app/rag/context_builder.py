from app.models.retrieval import SearchResult


def build_context(results: list[SearchResult]) -> str:
    """
    Build retrieval context.

    Args:
        results:
            Retrieved chunks

    Returns:
        Context string
    """

    sections: list[str] = []

    for result in results:
        sections.append(
            (
                f"[Video: "
                f"{result.external_id}]\n"
                f"[Chunk: "
                f"{result.chunk_id}]\n"
                f"{result.text}"
            )
        )

    return "\n\n".join(sections)
