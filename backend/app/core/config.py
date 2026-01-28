from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field, field_validator
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

    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def construct_database_url(cls, v, info):
        """
        If DATABASE_URL is not provided, construct it from individual fields.
        Otherwise, use the provided DATABASE_URL (from Render).
        """
        if v:
            # Convert postgres:// OR postgresql:// to postgresql+asyncpg:// for async driver
            if isinstance(v, str):
                if v.startswith('postgres://'):
                    return v.replace('postgres://', 'postgresql+asyncpg://', 1)
                elif v.startswith('postgresql://'):
                    return v.replace('postgresql://', 'postgresql+asyncpg://', 1)
            return v
        
        # Construct from individual fields
        data = info.data
        user = data.get('POSTGRES_USER')
        password = data.get('POSTGRES_PASSWORD')
        server = data.get('POSTGRES_SERVER')
        port = data.get('POSTGRES_PORT')
        db = data.get('POSTGRES_DB')
        
        if all([user, password, server, port, db]):
            return str(PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=user,
                password=password,
                host=server,
                port=port,
                path=db,
            ))
        
        raise ValueError(
            "Either DATABASE_URL or all of (POSTGRES_USER, POSTGRES_PASSWORD, "
            "POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB) must be provided"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
