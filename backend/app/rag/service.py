from app.llm.factory import get_llm
from app.models.chat import ChatResponse, SourceCitation
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_rag_prompt
from app.retrieval.search import search_chunks
from app.session.store import get_session


def ask_rag(
    *,
    session_id: str,
    query: str,
) -> ChatResponse:
    """
    Ask EngageAI.

    Args:
        session_id: Comparison session
        query: User question

    Returns:
        ChatResponse
    """

    session = get_session(session_id)

    if session is None:
        raise ValueError("Session not found")

    results = search_chunks(
        query=query,
        external_ids=[
            session.video_a.external_id,
            session.video_b.external_id,
        ],
        top_k=10,
    )

    transcript_context = build_context(results)

    prompt = build_rag_prompt(
        query=query,
        video_a=session.video_a,
        video_b=session.video_b,
        transcript_context=transcript_context,
    )

    llm = get_llm()
    response = llm.invoke(prompt)

    sources = [
        SourceCitation(
            external_id=result.external_id,
            chunk_id=result.chunk_id,
            text=result.text,
        )
        for result in results
    ]

    return ChatResponse(answer=str(response.content), sources=sources)
