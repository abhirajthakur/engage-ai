from collections.abc import AsyncGenerator

from app.graph.service import run_graph
from app.llm.factory import get_llm
from app.models.chat import ChatResult, SourceCitation
from app.session.memory import add_message


def chat(
    *,
    session_id: str,
    message: str,
) -> ChatResult:
    state = run_graph(
        session_id=session_id,
        query=message,
    )

    llm = get_llm()

    response = llm.invoke(state.prompt)

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
        sources=[
            SourceCitation(
                external_id=chunk.external_id,
                chunk_id=chunk.chunk_id,
                text=chunk.text,
            )
            for chunk in state.retrieved_chunks
        ],
    )


async def stream_chat(
    *,
    session_id: str,
    message: str,
) -> AsyncGenerator[str, None]:
    state = run_graph(
        session_id=session_id,
        query=message,
    )

    llm = get_llm()
    chunks: list[str] = []

    async for chunk in llm.astream(state.prompt):
        content = str(chunk.content)
        if not content:
            continue

        chunks.append(content)

        yield content

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
