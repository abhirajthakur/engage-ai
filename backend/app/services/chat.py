from collections.abc import AsyncGenerator
from dataclasses import dataclass

from app.graph.service import run_graph
from app.llm.factory import get_llm
from app.models.chat import ChatResult, SourceCitation
from app.schemas.chat import (
    DoneEvent,
    ErrorEvent,
    SourceCitationSchema,
    SourcesEvent,
    TokenEvent,
)
from app.services.sse import sse
from app.session.memory import add_message


@dataclass
class PreparedChat:
    prompt: str
    sources: list[SourceCitation]


def _prepare_chat(
    *,
    session_id: str,
    message: str,
) -> PreparedChat:
    """
    Shared chat preparation logic.

    Runs graph and builds citations.
    """

    state = run_graph(
        session_id=session_id,
        query=message,
    )

    sources = [
        SourceCitation(
            external_id=chunk.external_id,
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            platform=chunk.platform or "",
            title=chunk.title or "",
            creator=chunk.creator or "",
        )
        for chunk in state.retrieved_chunks
    ]

    return PreparedChat(
        prompt=state.prompt,
        sources=sources,
    )


def chat(
    *,
    session_id: str,
    message: str,
) -> ChatResult:
    prepared = _prepare_chat(
        session_id=session_id,
        message=message,
    )

    llm = get_llm()
    response = llm.invoke(prepared.prompt)
    answer = str(response.content)

    add_message(
        session_id=session_id,
        role="user",
        content=message,
    )

    add_message(
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    return ChatResult(
        answer=answer,
        sources=prepared.sources,
    )


async def stream_chat(
    *,
    session_id: str,
    message: str,
) -> AsyncGenerator[str, None]:
    try:
        prepared = _prepare_chat(
            session_id=session_id,
            message=message,
        )

        llm = get_llm()

        chunks: list[str] = []

        async for chunk in llm.astream(prepared.prompt):
            content = str(chunk.content)
            if not content:
                continue

            chunks.append(content)

            yield sse(TokenEvent(content=content))

        yield sse(
            SourcesEvent(
                sources=[
                    SourceCitationSchema(
                        external_id=source.external_id,
                        chunk_id=source.chunk_id,
                        text=source.text,
                        platform=source.platform,
                        title=source.title,
                        creator=source.creator,
                    )
                    for source in prepared.sources
                ]
            )
        )

        answer = "".join(chunks)

        add_message(
            session_id=session_id,
            role="user",
            content=message,
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        yield sse(DoneEvent())

    except Exception:
        yield sse(ErrorEvent(message="Internal server error"))
