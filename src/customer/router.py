from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from customer import crud, schemas
from db.models import Customer
from db.database import get_async_session
from customer import utilits
router = APIRouter()


# Получить список всех заказчиков
@router.get("/customers/")
async def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    query = select(Customer).offset(skip).limit(limit)
    result = await db.execute(query)
    customers = result.scalars().all()
    return customers


# Создать нового заказчика
@router.post("/customer/")
async def create_customer(
    customer: schemas.CustomerCreate,
    db: AsyncSession = Depends(get_async_session)
):
    cleaned_phone_number = await utilits.validate_phone_number(
       customer.phone_number, db)
    return await crud.create_customer(db, customer, cleaned_phone_number)


# Получить заказчика по phone_number
@router.get("/customers/{phone_number}",
            response_model=schemas.CustomerResponse)
async def read_customer(
    customer_id: str,
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.get_customer(db, customer_id)


# Обновить информацию о заказчике
@router.put("/customers/{phone_number}",
            response_model=schemas.CustomerUpdate)
async def update_customer(
    phone_number: str,
    customer: schemas.CustomerUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.update_customer(db, phone_number, customer)


# удалить заказчика
@router.delete("/customers/{phone_number}")
async def delete_customer(
    phone_number: str,
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.delete_customer(db, phone_number)
