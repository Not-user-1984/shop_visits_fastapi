from trade_points.routers import router as trade_router
from orders.routers import router as orders_router
from users.routers import router as user_router

from config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(trade_router)
app.include_router(orders_router)
app.include_router(user_router)