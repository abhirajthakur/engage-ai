from app.graph.graph import comparison_graph
from app.graph.state import GraphState


def run_graph(
    *,
    session_id: str,
    query: str,
) -> GraphState:
    state = GraphState(
        session_id=session_id,
        query=query,
    )

    result = comparison_graph.invoke(state)

    if isinstance(result, GraphState):
        return result

    return GraphState(**result)
