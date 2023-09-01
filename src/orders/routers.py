from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_async_session
from .crud import (
    create_order,
    update_order_status,
    get_orders,
)
from . import schemas
from db.models import OrderStatus
router = APIRouter()


# Маршруты для заказов
@router.post("/orders/", response_model=schemas.Order)
async def create_order_endpoint(
    order_data: schemas.OrderCreate,
    db: Session = Depends(get_async_session)
):
    order = await create_order(db, order_data)
    return order


@router.get("/orders/", response_model=list[schemas.OrderGetBase])
async def get_orders_endpoint(
    db: Session = Depends(get_async_session)
):
    orders = await get_orders(db)
    order_objects = [order[0] for order in orders]
    return order_objects


@router.put("/orders/{order_id}/status",
            response_model=schemas.OrderGetBase)
async def update_order_status_endpoint(
    order_id: int,
    new_status: OrderStatus,
    db: Session = Depends(get_async_session)
):
    order = await update_order_status(db, order_id, new_status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
