from app.models.session import ComparisonSession


_sessions: dict[
    str,
    ComparisonSession,
] = {}


def save_session(
    session: ComparisonSession,
) -> None:
    _sessions[session.session_id] = session


def get_session(
    session_id: str,
) -> ComparisonSession | None:
    return _sessions.get(session_id)
