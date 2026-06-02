from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.logging import get_logger
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    SourceCitationSchema,
)
from app.services.chat import chat, stream_chat
from app.session.service import get_session

logger = get_logger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        result = chat(
            session_id=request.session_id,
            message=request.message,
        )

        return ChatResponse(
            answer=result.answer,
            sources=[
                SourceCitationSchema(
                    external_id=source.external_id,
                    chunk_id=source.chunk_id,
                    text=source.text,
                )
                for source in result.sources
            ],
        )

    except ValueError as e:
        logger.warning("Invalid chat request: %s", str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        logger.exception("Unexpected error during chat", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


@router.post("/chat/stream")
async def stream_chat_endpoint(request: ChatRequest) -> StreamingResponse:
    try:
        session = get_session(request.session_id)

        if session is None:
            raise ValueError("Session not found")

        return StreamingResponse(
            stream_chat(
                session_id=request.session_id,
                message=request.message,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except ValueError as e:
        logger.warning("Invalid stream request: %s", str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        logger.exception("Unexpected error starting stream")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
