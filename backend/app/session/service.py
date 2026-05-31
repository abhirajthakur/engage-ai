from uuid import uuid4

from app.models.session import ComparisonSession
from app.session.store import save_session


def create_session(
    *, video_a_external_id: str, video_b_external_id: str
) -> ComparisonSession:
    session = ComparisonSession(
        session_id=str(uuid4()),
        video_a_external_id=video_a_external_id,
        video_b_external_id=video_b_external_id,
    )

    save_session(session)

    return session
