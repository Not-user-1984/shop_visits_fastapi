from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import Order
from . import schemas


# Создать заказ
async def create_order(
    db: Session,
    order_data: schemas.OrderCreate
):
    db_order = Order(**order_data.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


# Получить список заказов
async def get_orders(
    db: Session
):
    orders = await db.execute(select(Order))
    return orders.fetchall()


# Получить заказ по ID
async def _get_order(db: Session, order_id: int):
    order = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    return order.scalar_one_or_none()


# Обновить статус заказа
async def update_order_status(db: Session, order_id: int, new_status: str):
    db_order = await _get_order(db, order_id)
    if db_order:
        db_order.status = str(new_status)
        await db.commit()
        await db.refresh(db_order)
    return db_order
