from auth.routers import router as users_router

from config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(users_router)