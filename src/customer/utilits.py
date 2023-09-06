from sqlalchemy import select
from db.models import Customer
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_customer(
        db: AsyncSession,
        phone_number: str
) -> Customer:
    query = select(Customer).where(Customer.phone_number == phone_number)
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    return customer


async def check_customer_existence(db, phone_number):
    existing_customer = await get_customer(db, phone_number)
    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="The phone number already exists in the database")


async def validate_phone_number(phone_number: str, db: AsyncSession):
    # Убираем все символы, кроме цифр
    cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))
    # Проверяем длину номера телефона
    if len(cleaned_phone_number) < 9 or len(cleaned_phone_number) >= 50:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number length")
    return cleaned_phone_number
