from sqlalchemy import select
from sqlalchemy.orm import Session
from customer import schemas
from db.models import Customer

# Создать нового заказчика
async def create_customer(
        db: Session,
        customer: schemas.CustomerCreate):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

# Получить заказчика по ID
async def get_customer(db: Session, customer_id: int):
    query = select(Customer).where(Customer.id == customer_id)
    return await db.execute(query)

# Получить список всех заказчиков
async def get_customers(db: Session, skip: int = 0, limit: int = 100):
    query = select(Customer).offset(skip).limit(limit)
    return await db.execute(query)

# Обновить информацию о заказчике
async def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = await get_customer(db, customer_id)
    if db_customer:
        for key, value in customer.dict().items():
            setattr(db_customer.scalar_one(), key, value)
        await db.commit()
        await db.refresh(db_customer.scalar_one())
    return db_customer

# Удалить заказчика
async def delete_customer(db: Session, customer_id: int):
    db_customer = await get_customer(db, customer_id)
    if db_customer:
        await db.delete(db_customer.scalar_one())
        await db.commit()
    return db_customer.scalar_one()
