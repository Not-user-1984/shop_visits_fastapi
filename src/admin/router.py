from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import OrderStatus
from admin import schemas
from db.database import get_async_session
from db.models import Order

router = APIRouter()


@router.put("/order/{id_orders}", response_model=schemas.OrderResponse)
async def update_order_status(
    id_orders: int,
    data: OrderStatus,
    db: AsyncSession = Depends(get_async_session)
):

    order = await get_order_by_id(db, id_orders)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = data.value
    await db.commit()
    return order


async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
