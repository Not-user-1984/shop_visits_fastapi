from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from worker import schemas

from db.models import Worker


async def create_worker(
        db: AsyncSession,
        worker: schemas.WorkerCreate,
        cleaned_phone_number: str):
    db_worker = Worker(
        name=worker.name,
        phone_number=cleaned_phone_number,
        trade_point_id=worker.trade_point_id)
    db.add(db_worker)
    await db.commit()
    await db.refresh(db_worker)
    return db_worker


async def get_worker(db: AsyncSession, phone_number_id: int):
    stmt = select(Worker).where(Worker.phone_number == phone_number_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_workers(
        db: AsyncSession,
        skip: int = 0, limit: int = 10):
    stmt = select(Worker).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_worker(
        db: AsyncSession,
        worker_id: int,
        worker: schemas.WorkerUpdate):
    stmt = select(Worker).where(Worker.id == worker_id)
    result = await db.execute(stmt)
    db_worker = result.scalar_one_or_none()
    if db_worker:
        for key, value in worker.dict().items():
            setattr(db_worker, key, value)
        await db.commit()
        await db.refresh(db_worker)
    return db_worker


async def delete_worker(
        db: AsyncSession,
        worker_id: int):
    stmt = select(Worker).where(Worker.id == worker_id)
    result = await db.execute(stmt)
    db_worker = result.scalar_one_or_none()
    if db_worker:
        await db.delete(db_worker)
        await db.commit()
    return db_worker
