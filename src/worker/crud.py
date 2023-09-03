from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from worker import schemas
from typing import List

from db.models import Worker, Order
from fastapi import HTTPException


# Функция для поиска заказов через связь TradePoint
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
    worker = await get_worker_by_phone_number(db, phone_number)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Находим заказ по его ID
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Устанавливаем связь между заказом и работником
    order.executor_id = worker.id

    # Устанавливаем статус заказа в "in process"
    order.status = "in_process"

    # Сохраняем изменения в базе данных
    await db.commit()

    # Возвращаем обновленный заказ
    return order


async def get_worker_by_phone_number(db: AsyncSession, phone_number: str):
    stmt = select(Worker).where(Worker.phone_number == phone_number)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_order_by_id(db: AsyncSession, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_worker(
        db: AsyncSession,
        worker: schemas.WorkerCreate):
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    await db.commit()
    await db.refresh(db_worker)
    return db_worker

async def get_worker(db: AsyncSession, worker_id: int):
    stmt = select(Worker).where(Worker.id == worker_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_workers(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Worker).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_worker(db: AsyncSession, worker_id: int, worker: schemas.WorkerUpdate):
    stmt = select(Worker).where(Worker.id == worker_id)
    result = await db.execute(stmt)
    db_worker = result.scalar_one_or_none()
    
    if db_worker:
        for key, value in worker.dict().items():
            setattr(db_worker, key, value)
        await db.commit()
        await db.refresh(db_worker)
    return db_worker

async def delete_worker(db: AsyncSession, worker_id: int):
    stmt = select(Worker).where(Worker.id == worker_id)
    result = await db.execute(stmt)
    db_worker = result.scalar_one_or_none()
    
    if db_worker:
        db.delete(db_worker)
        await db.commit()
    return db_worker
