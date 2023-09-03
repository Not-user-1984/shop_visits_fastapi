from trade_points.routers import router as trade_router
# from orders.routers import router as orders_router
from customer.router import router as customer_router
from customer.orders.rourter import router as orders_customer_router
from worker.routers import router as worker_routers

from config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(trade_router)
# app.include_router(orders_router)
app.include_router(customer_router)
app.include_router(orders_customer_router)
app.include_router(worker_routers)
