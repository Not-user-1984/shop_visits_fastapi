from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import get_async_session

from worker.orders import logic, schemas

router = APIRouter()


# посмотреть заказы на точки
@router.get("/workers/orders/",
            response_model=List[schemas.OrderResponse])
async def get_worker_orders(
    phone_number: str,
    db: AsyncSession = Depends(get_async_session)
):
    orders = await logic.get_tradepoint_orders(db, phone_number)

    return orders


# выбрать заказ на выполение
@router.post("/workers/order_selection/{order_id}",
             response_model=schemas.OrderWorkerResponse)
async def assign_order(
    phone_number: str,
    order_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    order = await logic.assign_order_to_worker(db, phone_number, order_id)
    return order
