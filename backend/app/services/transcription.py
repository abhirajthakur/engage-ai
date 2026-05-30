from faster_whisper import WhisperModel

from app.core.logging import get_logger

logger = get_logger(__name__)

_model = None


def get_whisper_model() -> WhisperModel:
    global _model

    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    return _model


def transcribe_audio(
    audio_path: str,
) -> str:
    """
    Transcribe audio file.

    Args:
        audio_path: Audio file path

    Returns:
        str
    """

    logger.info(f"Transcribing {audio_path}")

    model = get_whisper_model()

    segments, info = model.transcribe(
        audio_path,
    )

    transcript = " ".join(segment.text for segment in segments)

    logger.info(f"Detected language: {info.language}")

    return transcript
