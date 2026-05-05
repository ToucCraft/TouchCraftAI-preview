import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Site Builder API"

    # Google Gemini
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-pro"
    GEMINI_MODEL_FAST: str = "gemini-2.5-flash"
    IMAGE_MODEL: str = "gemini-2.0-pro-exp-02-05"

    # S3 / MinIO
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_REGION: str = "auto"
    S3_PUBLIC_URL: str

    # Nginx Proxy Manager
    NPM_API_URL: str = "http://217.160.204.89:81/api"
    NPM_EMAIL: str = "NPM_EMAIL"
    NPM_PASSWORD: str = "NPM_PASSWORD"

    # SMTP & Auth
    SMTP_HOST: str = "SMTP_HOST"
    SMTP_PORT: int = 465
    SMTP_USER: str = "SMTP_USER"
    SMTP_PASSWORD: str = "SMTP_PASSWORD"

    ADMIN_EMAIL: str = "ADMIN_EMAIL"
    BASE_API_URL: str = "https://api-builder.touch-craft.com"

    AUTH0_DOMAIN: str = "AUTH0_DOMAIN"
    AUTH0_AUDIENCE: str = "https://api-builder.touch-craft.com"

    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    FRONTEND_URL: str

    GCP_PROJECT_ID: str = "gen-lang-client-0059231210"
    GCP_LOCATION: str = "us-central1"

    class Config:
        env_file = ".env"

settings = Settings()
