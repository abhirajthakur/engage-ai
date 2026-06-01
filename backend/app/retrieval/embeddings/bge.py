from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

    return _model


def embed_text(
    text: str,
) -> list[float]:
    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return embedding.tolist()


def embed_texts(
    texts: list[str],
) -> list[list[float]]:
    """
    Batch embedding generation.
    """

    if not texts:
        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    return embeddings.tolist()
