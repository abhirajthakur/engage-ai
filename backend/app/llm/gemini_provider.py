from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

_gemini_flash = None
_gemini_flash_lite = None


def get_gemini_flash() -> ChatGoogleGenerativeAI:
    """
    Returns Gemini 2.5 Flash.

    Returns:
        ChatGoogleGenerativeAI
    """
    global _gemini_flash

    if _gemini_flash is None:
        _gemini_flash = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0.2,
        )

    return _gemini_flash


def get_gemini_flash_lite() -> ChatGoogleGenerativeAI:
    """
    Returns Gemini 2.5 Flash Lite.

    Returns:
        ChatGoogleGenerativeAI
    """
    global _gemini_flash_lite

    if _gemini_flash_lite is None:
        _gemini_flash_lite = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.gemini_api_key,
            temperature=0.2,
        )

    return _gemini_flash_lite
