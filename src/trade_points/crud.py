from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.models import TradePoint

from . import schemas


# Создать торговую точку по ID
async def create_trade_point(
        db: AsyncSession,
        trade_point: schemas.TradePointCreate):

    existing_trade_point = await db.execute(
        select(TradePoint).where(TradePoint.name == trade_point.name)
    )

    if existing_trade_point.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Trade point with the same data already exists"
        )
    db_trade_point = TradePoint(**trade_point.dict())
    db.add(db_trade_point)
    await db.commit()
    await db.refresh(db_trade_point)
    return db_trade_point


# Получить торговую точку по ID
async def get_trade_point(db: AsyncSession, trade_point_id: int):
    trade_point = await db.execute(
        select(TradePoint).where(TradePoint.id == trade_point_id)
    )
    return trade_point.scalar_one_or_none()


# Получить список всех торговых точек
async def get_trade_points(db: AsyncSession):
    trade_points = await db.execute(select(TradePoint))
    return trade_points.scalars().all()


# Обновить информацию о торговой точке
async def update_trade_point(
        db: AsyncSession,
        trade_point_id: int,
        trade_point_data: schemas):
    db_trade_point = await get_trade_point(db, trade_point_id)
    if db_trade_point:
        for field, value in trade_point_data.dict().items():
            setattr(db_trade_point, field, value)
        await db.commit()
        await db.refresh(db_trade_point)
    return db_trade_point


# Удалить торговую точку
async def delete_trade_point(db: AsyncSession, trade_point_id: int):
    db_trade_point = await get_trade_point(db, trade_point_id)
    if db_trade_point:
        await db.delete(db_trade_point)
        await db.commit()
    return db_trade_point

