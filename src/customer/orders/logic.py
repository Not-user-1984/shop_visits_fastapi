from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from db.models import Order, Customer, TradePoint
from fastapi import HTTPException

# Функция для создания заказа клиентом
async def create_order(db: Session, customer_id: int, order_data: dict) -> Order:
    # Проверяем, существует ли клиент с заданным customer_id
    customer = await get_customer(db, customer_id)
    if not customer:
        raise ValueError("Customer not found")

    # Создаем новый заказ и связываем его с клиентом
    order = Order(**order_data, author=customer)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


# Функция для удаления заказа клиентом
async def delete_order(db: Session, customer_id: int, order_id: int) -> bool:
    # Проверяем, существует ли клиент с заданным customer_id
    customer = await get_customer(db, customer_id)
    if not customer:
        raise ValueError("Customer not found")
    # Проверяем, существует ли заказ с заданным order_id и является ли он заказом этого клиента
    order = await get_order(db, order_id)
    if not order or order.author_id != customer_id:
        raise ValueError("Order not found")

    # Удаляем заказ
    db.delete(order)
    await db.commit()
    return True


# Функция для получения всех заказов клиента
async def get_customer_orders(db: Session, customer_id: int) -> List[Order]:
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
async def get_customer(db: Session, customer_id: int) -> Customer:
    stmt = select(Customer).where(Customer.id == customer_id)
    result = await db.execute(stmt)
    return result.scalar()

# Функция для получения заказа по ID
async def get_order(db: Session, order_id: int) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    return result.scalar()


async def get_customer_by_phone_number_and_trade_point(
        db: Session,
        phone_number: str,
        trade_point_id: int) -> Customer:
    # Поиск клиента по номеру телефона
    stmt = select(Customer).where(
        Customer.phone_number == phone_number,
        Customer.trade_point_id == trade_point_id)
    result = await db.execute(stmt)
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer

# async def get_trade_point(db: Session, trade_point_id: int, customer_id: int) -> TradePoint:
#     # Поиск торговой точки по ID и проверка, что она принадлежит данному клиенту
#     stmt = select(Customer).where(
#         TradePoint.id == trade_point_id,
#         TradePoint.customer_id == customer_id
#     )
#     result = await db.execute(stmt)
#     trade_point = result.scalar_one_or_none()

#     if not trade_point:
#         raise HTTPException(status_code=400, detail="Trade point not found or does not belong to the customer")

#     return trade_point
