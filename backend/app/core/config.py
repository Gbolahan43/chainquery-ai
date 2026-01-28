from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field, field_validator, model_validator
from typing import Literal, Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ChainQuery AI"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    
    # Database - Accept DATABASE_URL from Render or individual components
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_DB: Optional[str] = None
    
    # AI - Make at least one required
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"  # Override in .env for production

    @model_validator(mode='after')
    def assemble_db_connection(self) -> "Settings":
        v = self.DATABASE_URL
        if isinstance(v, str):
            # Convert postgres:// OR postgresql:// to postgresql+asyncpg:// for async driver
            if v.startswith('postgres://'):
                self.DATABASE_URL = v.replace('postgres://', 'postgresql+asyncpg://', 1)
            elif v.startswith('postgresql://'):
                self.DATABASE_URL = v.replace('postgresql://', 'postgresql+asyncpg://', 1)
            return self

        # Construct from individual fields if DATABASE_URL is missing
        if self.POSTGRES_SERVER and self.POSTGRES_PORT and self.POSTGRES_USER and self.POSTGRES_DB:
            self.DATABASE_URL = str(PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            ))
            return self
        
        raise ValueError(
            "Either DATABASE_URL or all of (POSTGRES_USER, POSTGRES_PASSWORD, "
            "POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB) must be provided"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
