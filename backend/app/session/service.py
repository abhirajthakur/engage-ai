from uuid import uuid4

from app.models.session import ComparisonSession
from app.models.video import VideoData
from app.session.store import get_session as get_session_from_store
from app.session.store import save_session


def create_session(
    *,
    video_a: VideoData,
    video_b: VideoData,
) -> ComparisonSession:
    session = ComparisonSession(
        session_id=str(uuid4()),
        video_a=video_a,
        video_b=video_b,
    )

    save_session(session)

    return session


def get_session(session_id: str) -> ComparisonSession | None:
    return get_session_from_store(session_id)
