def build_rag_prompt(
    *,
    query: str,
    context: str,
) -> str:
    """
    Build EngageAI RAG prompt.
    """

    return f"""
You are EngageAI.

You analyze and compare
social media videos.

Answer ONLY using
the provided context.

If information is not
available in the context,
say so.

Always be specific.

Context:
{context}

Question:
{query}
"""
