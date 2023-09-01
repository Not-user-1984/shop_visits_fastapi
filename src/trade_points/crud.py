from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import TradePoint, Order, Worker
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


# Получить торговую точку по ID
async def get_trade_point(db: Session, trade_point_id: int):
    trade_point = await db.execute(
        select(TradePoint).where(TradePoint.id == trade_point_id)
    )
    return trade_point.scalar_one_or_none()


# Создать торговую точку по ID
async def create_trade_point(
        db: Session,
        trade_point: schemas.TradePointCreate):
    db_trade_point = TradePoint(**trade_point.dict())
    db.add(db_trade_point)
    await db.commit()
    await db.refresh(db_trade_point)
    return db_trade_point


# Получить список всех торговых точек
async def get_trade_points(db: Session):
    trade_points = await db.execute(select(TradePoint))
    return trade_points.scalars().all()


# Обновить информацию о торговой точке
async def update_trade_point(
        db: Session,
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
async def delete_trade_point(db: Session, trade_point_id: int):
    db_trade_point = await get_trade_point(db, trade_point_id)
    if db_trade_point:
        await db.delete(db_trade_point)
        await db.commit()
    return db_trade_point


# Получить заказ по ID
async def _get_order(db: Session, order_id: int):
    order = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    return order.scalar_one_or_none()


# Обновить статус заказа
async def update_order_status(db: Session, order_id: int, new_status: str):
    db_order = await _get_order(db, order_id)
    if db_order:
        db_order.status = new_status
        await db.commit()
        await db.refresh(db_order)
    return db_order
