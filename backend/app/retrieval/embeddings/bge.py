from app.core.logging import get_logger
import json

from sentence_transformers import SentenceTransformer

from app.cache.factory import get_cache
from app.cache.keys import embedding_key

_model = None


logger = get_logger(__name__)


def get_embedding_model() -> SentenceTransformer:
    global _model

    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

    return _model


def embed_text(
    text: str,
) -> list[float]:

    cache = get_cache()
    key = embedding_key(text)

    cached = cache.get(
        key,
    )

    if cached is not None:
        logger.info("Embedding cache hit")
        return json.loads(cached)

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embedding_list = embedding.tolist()

    cache.set(
        key,
        json.dumps(
            embedding_list,
        ),
    )

    return embedding_list
