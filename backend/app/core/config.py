from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field
from typing import Literal

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ChainQuery AI"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    
    # Database Credentials
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # AI
    OPENAI_API_KEY: str
    GROQ_API_KEY: str | None = None

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the Async Postgres URL from individual fields.
        Format: postgresql+asyncpg://user:pass@host:port/db
        """
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
