from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List
from worker import utilits
from db.models import Worker, Order
from fastapi import HTTPException


async def get_tradepoint_orders(
        db: AsyncSession, phone_number: str) -> List[Order]:

    # Сначала найдем работника по номеру телефона
    stmt_worker = select(Worker).where(Worker.phone_number == phone_number)
    result_worker = await db.execute(stmt_worker)
    worker = result_worker.scalar_one_or_none()

    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Затем найдем торговую точку работника
    trade_point = worker.trade_point_id

    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade point not found")

    # найдем все заказы на этой торговой точке
    stmt_orders = select(Order).where(Order.where_id == trade_point)
    result_orders = await db.execute(stmt_orders)
    orders = result_orders.scalars().all()

    return orders


async def assign_order_to_worker(
    db: AsyncSession,
    phone_number: str,
    order_id: int
):
    # Находим работника по номеру телефона
    worker = await utilits.get_worker_by_phone_number(db, phone_number)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Проверяем, что работник не заблокирован
    if worker.is_blocked:
        raise HTTPException(
            status_code=400,
            detail="Worker is blocked and cannot accept orders")

    # Находим заказ по его ID
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Устанавливаем связь между заказом и работником
    order.executor_id = worker.id

    # Устанавливаем статус заказа в "in process"
    order.status = "in_process"
    worker.is_blocked = True

    # Сохраняем изменения в базе данных
    await db.commit()

    # Возвращаем обновленный заказ
    return order


async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
