from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from customer.orders import logic, validation
from db.database import get_async_session

from . import logic, schemas

router = APIRouter()


# Создать заказ клиентом
@router.post("/customers/create_orders/", response_model=schemas.OrderResponse)
async def create_order(
    order_data: schemas.OrderCreate,
    db: AsyncSession = Depends(get_async_session)
):
    # Поиск клиента по номеру телефона
    customer = await logic.get_customer_by_phone(db, order_data.phone_number)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Проверяем существование заказа с такими же данными
    if await validation.order_exists(db, order_data, customer.id):
        raise HTTPException(status_code=404, detail="order not yet processed")

    order = await logic.create_order_in_db(db, order_data, customer.id)
    return order


@router.post("/customers/visit/{order_id}",
             response_model=schemas.VisitResponse)
async def complete_order_and_unlock_worker(
    phone_number: str,
    order_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    return await logic.complete_order_and_unlock_worker(
        db, phone_number, order_id
        )


@router.delete("/customers/orders/{order_id}")
async def delete_order(
    order_data: schemas.OrderDelete,
    order_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    try:
        await logic.delete_order(db, order_data.phone_number, order_id)
        return {"message": "Order deleted successfully"}
    except HTTPException as e:
        # Здесь можно добавить логирование ошибки, если необходимо
        raise e


# Получить все заказы клиента
@router.get("/customers/{customer_id}/orders/",
            response_model=schemas.CustomerOrdersResponse)
async def get_customer_orders(
    customer_id: int, db: AsyncSession = Depends(get_async_session)
):
    customer = await logic.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    orders = await logic.get_customer_orders(db, customer_id)
    return {"customer": customer, "orders": orders}
