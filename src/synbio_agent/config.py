from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    OLLAMA_MODEL: str = "gemma3:4b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/synbio_latam_db"


settings = Settings()