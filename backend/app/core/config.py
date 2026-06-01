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
    environment: str = "development"
    api_prefix: str = "/api"


settings = Settings()  # ty:ignore[missing-argument]
