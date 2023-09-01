from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import Worker, Customer, Visit
from . import schemas


# Получить список торговых точек, привязанных к номеру телефона работника
async def get_trade_points_by_worker_phone(
        db: Session, phone_number: str
        ):
    worker = await db.execute(
        select(Worker).where(Worker.phone_number == phone_number)
    )
    worker = worker.scalar_one_or_none()
    if not worker:
        return []
    trade_points = worker.trade_points
    return trade_points


# Создать сотрудника
async def create_worker(
    db: Session,
    worker_data: schemas.WorkerCreate
):
    db_worker = Worker(**worker_data.dict())
    db.add(db_worker)
    await db.commit()
    await db.refresh(db_worker)
    return db_worker


# Получить список сотрудников
async def get_workers(
    db: Session
):
    workers = await db.execute(select(Worker))
    return workers.fetchall()


# Создать заказчика
async def create_customer(
    db: Session,
    customer_data: schemas.CustomerCreate
):
    db_customer = Customer(**customer_data.dict())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


# Получить список заказчиков
async def get_customers(
    db: Session
):
    customers = await db.execute(select(Customer))
    return customers.fetchall()


# Создать посещение
async def create_visit(
    db: Session,
    visit_data: schemas.VisitCreate
):
    db_visit = Visit(**visit_data.dict())
    db.add(db_visit)
    await db.commit()
    await db.refresh(db_visit)
    return db_visit


# Получить список посещений
async def get_visits(
    db: Session
):
    visits = await db.execute(select(Visit))
    return visits.fetchall()
