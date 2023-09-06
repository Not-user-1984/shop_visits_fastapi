from sqlalchemy import select

from db.models import Worker
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def validate_phone_number(phone_number: str, db: AsyncSession):
    # Убираем все символы, кроме цифр
    cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))

    # Проверяем длину номера телефона
    if len(cleaned_phone_number) < 9 or len(cleaned_phone_number) >= 50:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number length")
    # Проверяем уникальность номера телефона в базе данных
    existing_worker = await get_worker_by_phone_number(
        db, cleaned_phone_number)
    if existing_worker:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    return cleaned_phone_number


async def get_worker_by_phone_number(db: AsyncSession, phone_number: str):
    stmt = select(Worker).where(Worker.phone_number == phone_number)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()