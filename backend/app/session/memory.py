import json

from app.cache.factory import get_cache
from app.cache.keys import conversation_cache_key
from app.core.config import settings
from app.models.message import ChatMessage


def get_messages(session_id: str) -> list[ChatMessage]:
    """
    Load conversation history.
    """

    cache = get_cache()
    data = cache.get(conversation_cache_key(session_id))

    if data is None:
        return []

    raw_messages: list[dict] = json.loads(data)

    return [ChatMessage.model_validate(message) for message in raw_messages]


def add_message(
    *,
    session_id: str,
    role: str,
    content: str,
) -> None:
    """
    Append message to conversation.
    """

    messages = get_messages(session_id)

    messages.append(
        ChatMessage(
            role=role,
            content=content,
        ),
    )

    cache = get_cache()

    cache.set(
        key=conversation_cache_key(session_id),
        value=json.dumps([message.model_dump() for message in messages]),
        ttl_seconds=settings.session_ttl_seconds,
    )


def clear_messages(session_id: str) -> None:
    """
    Delete conversation history.
    """

    cache = get_cache()

    cache.delete(conversation_cache_key(session_id))
