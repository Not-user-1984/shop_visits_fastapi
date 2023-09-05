from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from worker.orders import logic


async def validate_phone_number(phone_number: str, db: AsyncSession):
    # Убираем все символы, кроме цифр
    cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))

    # Проверяем длину номера телефона
    if len(cleaned_phone_number) < 9 or len(cleaned_phone_number) >= 50:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number length")
    # Проверяем уникальность номера телефона в базе данных
    existing_worker = await logic.get_worker_by_phone_number(db, cleaned_phone_number)
    if existing_worker:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    return cleaned_phone_number
