from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "Area Todo API"
    debug: bool = False
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/area_todo"
    )
    cors_origins: list[str] = ["http://localhost:3000"]
    jwt_secret: str = "dev-only-change-me-use-32chars-min"
    jwt_algorithm: str = "HS256"
    jwt_expires_seconds: int = 86400



settings = Settings()
