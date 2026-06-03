from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    port: int = 8000
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
