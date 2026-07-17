from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str 

    # Security & JWT Settings
    # Generate a secure key using: openssl rand -hex 32
    SECRET_KEY: str = "b4f2c9b4e5d6b4f2c9b4e5d6b4f2c9b4e5d6b4f2c9b4e5d6b4f2c9b4e5d6b4f2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30 # 30 days
    
    # Email Settings
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "My FastAPI App"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    FRONTEND_URL: str = "http://localhost:3000"

    # Pydantic V2 professional configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore" # Ignore extra env vars not defined in the class
    )

settings = Settings()
