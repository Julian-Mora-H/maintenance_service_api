from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # leer .env
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "Maintenance Service API"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./maintenance.db"
    AWS_S3_BUCKET: str = "mi-bucket-simulado"
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

settings = Settings()