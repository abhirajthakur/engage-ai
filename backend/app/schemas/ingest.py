import re

from pydantic import BaseModel, field_validator, model_validator

from app.models.video import VideoData

YT_SHORTS_PATTERNS = [
    r"youtube\.com/shorts/[\w-]+",
    r"youtu\.be/[\w-]+",  # short link redirects can be shorts too
]

IG_REEL_PATTERNS = [
    r"instagram\.com/reel/[\w-]+",
    r"instagram\.com/reels/[\w-]+",
]


def _matches_any(url: str, patterns: list[str]) -> bool:
    return any(re.search(p, url) for p in patterns)


class IngestRequest(BaseModel):
    youtube_url: str
    instagram_url: str

    @field_validator("youtube_url")
    @classmethod
    def validate_youtube(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("YouTube URL cannot be empty")
        if not _matches_any(value, YT_SHORTS_PATTERNS):
            raise ValueError(
                "Invalid YouTube URL. Must be a YouTube Shorts link "
                "(e.g. youtube.com/shorts/<id>)"
            )
        return value

    @field_validator("instagram_url")
    @classmethod
    def validate_instagram(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Instagram URL cannot be empty")
        if not value.startswith("https://"):
            raise ValueError("Instagram URL must start with https://")
        if not _matches_any(value, IG_REEL_PATTERNS):
            raise ValueError(
                "Invalid Instagram URL. Must be a Reel link "
                "(e.g. instagram.com/reel/<id>)"
            )
        return value

    @model_validator(mode="after")
    def no_duplicate_urls(self) -> "IngestRequest":
        if self.youtube_url == self.instagram_url:
            raise ValueError("YouTube and Instagram URLs must be different")
        return self


class IngestResponse(BaseModel):
    session_id: str
    video_a: VideoData
    video_b: VideoData
