from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from customer import crud, schemas
from db.models import Customer
from db.database import get_async_session

router = APIRouter()

# Получить список всех заказчиков (асинхронно)
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

# Создать нового заказчика (асинхронно)
@router.post("/customers/")
async def create_customer(customer: schemas.CustomerCreate, db: AsyncSession = Depends(get_async_session)):
    return await crud.create_customer(db, customer)

# Получить заказчика по ID (асинхронно)
@router.get("/customers/{customer_id}")
async def read_customer(customer_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Customer).where(Customer.id == customer_id)
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Обновить информацию о заказчике (асинхронно)
@router.put("/customers/{customer_id}")
async def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: AsyncSession = Depends(get_async_session)):
    updated_customer = await crud.update_customer(db, customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer.scalar_one()

# Удалить заказчика (асинхронно)
@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_async_session)):
    deleted_customer = await crud.delete_customer(db, customer_id)
    if not deleted_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted_customer.scalar_one()
