import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Fast api"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "db")
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?async_fallback=True"
    app_title: str = 'shop_visit'
    description: str = 'shop_visit'


settings = Settings()
