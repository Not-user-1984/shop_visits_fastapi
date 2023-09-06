from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from customer import schemas
from db.models import Customer

from customer.utilits import check_customer_existence, get_customer


# Создать нового заказчика
async def create_customer(
        db: AsyncSession,
        customer: schemas.CustomerCreate,
        cleaned_phone_number: str):

    await check_customer_existence(db, cleaned_phone_number)

    db_customer = Customer(
        name=customer.name,
        phone_number=cleaned_phone_number,
    )
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


# Получить список всех заказчиков
async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Customer).offset(skip).limit(limit)
    return await db.execute(query)


# Обновить информацию о заказчике
async def update_customer(
        db: AsyncSession,
        phone_number: str,
        customer: schemas.CustomerUpdate
        ):
    await check_customer_existence(db, customer.phone_number)
    db_customer = await get_customer(db, phone_number)
    if db_customer:
        for key, value in customer.dict().items():
            setattr(db_customer, key, value)
        await db.commit()
        await db.refresh(db_customer)
    else:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


# Удалить заказчика
async def delete_customer(db: AsyncSession, phone_number: str):
    db_customer = await get_customer(db, phone_number)
    if db_customer:
        await db.delete(db_customer)
        await db.commit()
        return HTTPException(
            status_code=200, detail="Customer deleted successfully")
    raise HTTPException(status_code=404, detail="Customer not found")
