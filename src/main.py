from trade_points.routers import router as trade_router
from orders.routers import router as orders_router
from workers_customers.routers import router as workers_customers_router

from config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(trade_router)
app.include_router(orders_router)
app.include_router(workers_customers_router)