from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from db.models import Order, Customer


async def order_exists(db: Session, order_data: dict) -> bool:
    stmt = select(Order).where(
        Order.phone_number == order_data['phone_number'],
        Order.trade_point_id == order_data['trade_point_id'],
        Order.ended_at == order_data['ended_at']
    )
    result = await db.execute(stmt)
    existing_order = await result.scalar_one_or_none()
    return existing_order is not None


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
        raise HTTPException(
            status_code=404,
            detail="Customer not found")
    return customer