from pydantic import BaseModel


def sse(event: BaseModel) -> str:
    """
    Convert model to SSE payload.
    """

    return f"data: {event.model_dump_json()}\n\n"
