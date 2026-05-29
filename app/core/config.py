from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    gemini_api_key: str

    apify_api_token: str

    # App
    log_level: str = "INFO"
    environment: str = "development"
    api_prefix: str = "/api"


settings = Settings()  # ty:ignore[missing-argument]
