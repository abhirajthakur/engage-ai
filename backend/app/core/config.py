from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    gemini_api_key: str
    groq_api_key: str

    # Hugging Face Hub (for embeddings)
    hf_token: str | None = None

    # Vector DB
    vector_db: str = "chroma"

    # Apify
    apify_api_token: str

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Cache
    cache_provider: str = "disk"
    session_ttl_seconds: int = 60 * 60 * 24

    # App
    log_level: str = "INFO"
    environment: Literal["development", "staging", "production"] = "development"
    api_prefix: str = "/api"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )


settings = Settings()  # ty:ignore[missing-argument]
