from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    build_prompt_node,
    load_memory_node,
    load_session_node,
    retrieve_node,
)
from app.graph.state import GraphState

builder = StateGraph(GraphState)

builder.add_node("load_session", load_session_node)
builder.add_node("load_memory", load_memory_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("build_prompt", build_prompt_node)

builder.add_edge(START, "load_session")
builder.add_edge("load_session", "load_memory")
builder.add_edge("load_memory", "retrieve")
builder.add_edge("retrieve", "build_prompt")
builder.add_edge("build_prompt", END)

comparison_graph = builder.compile()
