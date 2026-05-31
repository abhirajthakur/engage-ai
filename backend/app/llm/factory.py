from langchain_core.runnables import RunnableWithFallbacks

from app.llm.gemini_provider import get_gemini_flash, get_gemini_flash_lite
from app.llm.groq_provider import get_groq_70b


def get_llm() -> RunnableWithFallbacks:
    """
    Returns production-ready LLM fallback chain.

    Order:
    Gemini Flash
        ↓
    Gemini Flash Lite
        ↓
    Groq Llama 3.3 70B
        ↓
    Groq Llama 3.1 8B

    Returns:
        RunnableWithFallbacks
    """

    gemini_flash = get_gemini_flash().with_retry()
    gemini_flash_lite = get_gemini_flash_lite().with_retry()

    groq_70b = get_groq_70b().with_retry()

    return gemini_flash.with_fallbacks([gemini_flash_lite, groq_70b])
