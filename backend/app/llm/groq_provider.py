from langchain_groq import ChatGroq
from pydantic import SecretStr

from app.core.config import settings

_groq_70b = None
_groq_8b = None


def get_groq_70b() -> ChatGroq:
    """
    Returns Llama 3.3 70B.

    Returns:
        ChatGroq
    """

    global _groq_70b

    if _groq_70b is None:
        _groq_70b = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=SecretStr(settings.groq_api_key),
            temperature=0.2,
        )

    return _groq_70b
