from fastapi import FastAPI
from sqladmin import Admin

from admin import models
from config import settings
from customer.orders.rourter import router as orders_customer_router
from customer.router import router as customer_router
from db.database import engine
from trade_points.routers import router as trade_router
from worker.orders.routers import router as orders_worker_routers
from worker.routers import router as worker_routers

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)


app.include_router(trade_router, tags=["Trade crud"])
app.include_router(customer_router, tags=["Customer crud"])
app.include_router(orders_customer_router, tags=["Customer orders"])
app.include_router(worker_routers, tags=["Worker crud"])
app.include_router(orders_worker_routers, tags=["Worker orders"])

admin = Admin(app, engine)

admin.add_view(models.WorkerAdmin)
admin.add_view(models.CustomerAdmin)
admin.add_view(models.VisitAdmin)
admin.add_view(models.TradePointAdmin)
admin.add_view(models.OrderAdmin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)