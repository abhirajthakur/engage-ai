from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.logging import get_logger
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    SourceCitationSchema,
)
from app.services.chat import chat, stream_chat

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
        logger.exception("Unexpected error during chat")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


@router.post("/chat/stream")
async def stream_chat_endpoint(request: ChatRequest):
    try:
        return StreamingResponse(
            stream_chat(
                session_id=request.session_id,
                message=request.message,
            ),
            media_type="text/plain",
        )

    except ValueError as e:
        logger.warning("Invalid stream request: %s", str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        logger.exception("Unexpected error during stream chat")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
