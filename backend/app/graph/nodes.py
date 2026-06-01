from app.graph.prompt_builder import build_prompt
from app.graph.state import GraphState
from app.retrieval.search import search_chunks
from app.session.memory import get_messages
from app.session.service import get_session


def load_session_node(state: GraphState) -> GraphState:
    session = get_session(state.session_id)

    if session is None:
        raise ValueError("Session not found")

    state.video_a = session.video_a
    state.video_b = session.video_b

    return state


def load_memory_node(state: GraphState) -> GraphState:
    """
    Load conversation history.
    """
    state.messages = get_messages(state.session_id)

    return state


def retrieve_node(state: GraphState) -> GraphState:
    if state.video_a is None or state.video_b is None:
        raise ValueError("Videos not loaded")

    state.retrieved_chunks = search_chunks(
        query=state.query,
        external_ids=[
            state.video_a.external_id,
            state.video_b.external_id,
        ],
        top_k=10,
    )

    return state


def build_prompt_node(state: GraphState) -> GraphState:
    if state.video_a is None or state.video_b is None:
        raise ValueError("Videos not loaded")

    transcript_context = "\n\n".join(chunk.text for chunk in state.retrieved_chunks)

    conversation_history = "\n".join(
        (f"{message.role}: {message.content}") for message in state.messages
    )

    state.prompt = build_prompt(
        query=state.query,
        video_a=state.video_a,
        video_b=state.video_b,
        transcript_context=transcript_context,
        conversation_history=conversation_history,
    )

    return state
