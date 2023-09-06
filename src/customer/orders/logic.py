from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from customer.orders import schemas
from db.models import Customer, Order, Visit, Worker


# Функция для создания заказа клиентом
async def create_order_in_db(
        db: AsyncSession,
        order_data:  schemas.OrderCreate,
        customer_id: int) -> Order:
    expiration_date = datetime.utcnow() + timedelta(days=7)
    order = Order(
        created_at=datetime.utcnow(),
        ended_at=expiration_date,
        where_id=order_data.trade_point_id,
        author_id=customer_id,
        status="started"
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


# Функция для создания визита клиентом
async def complete_order_and_unlock_worker(
    db: AsyncSession,
    phone_number: str,
    order_id: int,
):
    # Находим Customer по номеру телефона и проверяем, что он существует в базе
    stmt_customer = select(Customer).where(
        Customer.phone_number == phone_number)
    customer_odj = await db.execute(stmt_customer)
    customer = customer_odj.scalar()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # находим заказ по ID
    stmt_order = select(Order).where(Order.id == order_id)
    order = await db.execute(stmt_order)
    order = order.scalar()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Проверяем, что время заказа не кончилось
    if order.ended_at <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Order has ended")

    # находим Worker
    stmt_worker = select(Worker).where(Worker.id == order.executor_id)
    worker_odj = await db.execute(stmt_worker)
    worker = worker_odj.scalar()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Создаем новую запись в таблице Visit
    visit = Visit(
        created_at=datetime.utcnow(),
        executor_id=worker.id,
        order_id=order.id,
        author_id=order.author_id,
        where_id=order.where_id
    )
    db.add(visit)
    # Разблокируем работника
    worker.is_blocked = False
    order.status = "ended"
    await db.commit()

    return visit


async def delete_order(
        db: AsyncSession,
        phone_number: int,
        order_id: int) -> bool:

    customer = await get_customer_by_phone(db, phone_number)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = await get_order(db, order_id)
    if not order or order.author_id != customer.id:
        raise HTTPException(status_code=404, detail="Order not found")
    if await get_order_status(db, order_id):
            await db.delete(order)
            await db.commit()
            return True
    raise HTTPException(
        status_code=404,
        detail="Only completed orders can be deleted")


# Функция для получения всех заказов клиента
async def get_customer_orders(
        db: AsyncSession, customer_id: int) -> List[Order]:
    # Проверяем, существует ли клиент с заданным customer_id
    customer = await get_customer(db, customer_id)
    if not customer:
        raise ValueError("Customer not found")

    # Получаем все заказы, созданные этим клиентом
    stmt = select(Order).where(Order.author_id == customer_id)
    result = await db.execute(stmt)
    orders = result.scalars().all()
    return orders


# Функция для получения клиента по ID
async def get_customer(db: AsyncSession, customer_id: int) -> Customer:
    stmt = select(Customer).where(Customer.id == customer_id)
    result = await db.execute(stmt)
    return result.scalar()


# Функция для получения заказа по ID
async def get_order(db: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(
        Order.id == order_id,
)
    result = await db.execute(stmt)
    return result.scalar()


# Функция для получения статуса заказа по ID
async def get_order_status(db: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(
        Order.status == "started")
    result = await db.execute(stmt)
    return result.scalar()


# Поиск клиента по номеру телефона
async def get_customer_by_phone(
        db: AsyncSession,
        phone_number: str,) -> Customer:
    stmt = select(Customer).where(
        Customer.phone_number == phone_number,
    )
    result = await db.execute(stmt)
    customer = result.scalar_one_or_none()
    return customer
