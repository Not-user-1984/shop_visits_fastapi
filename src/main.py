from fastapi import FastAPI
from sqladmin import Admin

from admin import models_view
from config import settings
from customer.orders.rourter import router as orders_customer_router
from customer.router import router as customer_router
from db.database import engine
from trade_points.routers import router as trade_router
from worker.orders.router import router as orders_worker_routers
from worker.router import router as worker_routers
from admin.router import router as admin_routers
app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)


app.include_router(trade_router, tags=["Trade crud"])
app.include_router(customer_router, tags=["Customer crud"])
app.include_router(orders_customer_router, tags=["Customer orders"])
app.include_router(worker_routers, tags=["Worker crud"])
app.include_router(orders_worker_routers, tags=["Worker orders"])
app.include_router(admin_routers, tags=["PUT status order"])

admin = Admin(app, engine)

admin.add_view(models_view.WorkerAdmin)
admin.add_view(models_view.CustomerAdmin)
admin.add_view(models_view.VisitAdmin)
admin.add_view(models_view.TradePointAdmin)
admin.add_view(models_view.OrderAdmin)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
