from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Set to 'true' to use in-memory SQLite (no Postgres). Good for study demos on Render without a DB."""
    DISABLE_DB: str = "false"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/llm_lab"
    """Set to 'true' on Render (and other hosted Postgres) to use SSL."""
    DATABASE_SSL: str = "false"
    """Set to 'true' on Render/hosted to disable the heavy fine-tune demo (avoids 502 timeouts)."""
    DISABLE_FINETUNE_DEMO: str = "false"
    SECRET_KEY: str = "change-this-to-a-random-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DEEPSEEK_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    HF_MODEL_NAME: str = "google/flan-t5-small"

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
