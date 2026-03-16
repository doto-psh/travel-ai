from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    JWT_SECRET_KEY: str = "your-secret-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    BACKEND_PORT: int = 18000
    FRONTEND_PORT: int = 15173
    CORS_ORIGINS: str = "http://localhost:15173"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
