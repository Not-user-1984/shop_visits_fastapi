from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, logic
from db.database import get_async_session

from datetime import datetime, timedelta
from db.models import Order

router = APIRouter()


# Создать заказ клиентом
@router.post("/orders/", response_model=schemas.OrderResponse)
async def create_order(
    order_data: schemas.OrderCreate, db: Session = Depends(get_async_session)
):
    # Поиск клиента по номеру телефона
    customer = await logic.get_customer_by_phone_number_and_trade_point(
        db,
        order_data.phone_number,
        order_data.trade_point_id
        )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Вычисление даты истечения заказа (+7 дней от создания заказа)
    expiration_date = datetime.utcnow() + timedelta(days=7)

    # Создание нового заказа с заданными данными
    order = Order(
        created_at=datetime.utcnow(),
        ended_at=expiration_date,
        where_id=order_data.trade_point_id,
        author_id=customer.id,
        status="started"  # Начальный статус заказа
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


# Удалить заказ клиентом
@router.delete("/customers/{customer_id}/orders/{order_id}")
async def delete_order(
    customer_id: int, order_id: int, db: Session = Depends(get_async_session)
):
    result = logic.delete_order(db, customer_id, order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# Получить все заказы клиента
@router.get("/customers/{customer_id}/orders/", response_model=schemas.CustomerOrdersResponse)
async def get_customer_orders(
    customer_id: int, db: Session = Depends(get_async_session)
):
    customer = logic.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    orders = logic.get_customer_orders(db, customer_id)
    return {"customer": customer, "orders": orders}
