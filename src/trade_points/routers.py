from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_async_session
from .crud import (
    create_trade_point,
    get_trade_point,
    get_trade_points,
    update_trade_point,
    delete_trade_point,
    update_order_status,
    get_trade_points_by_worker_phone
)
from . import schemas

router = APIRouter()


# Получить список торговых точек по номеру телефона работника
@router.get("/trade_points_by_worker/{phone_number}",
            response_model=list[schemas.TradePoint])
async def get_trade_points_by_worker_phone_endpoint(
    phone_number: str,
    db: Session = Depends(get_async_session)
):
    trade_points = await get_trade_points_by_worker_phone(db, phone_number)
    return trade_points


# Создать торговую точку
@router.post("/trade_points/", response_model=schemas.TradePoint)
async def create_trade_point_endpoint(
    trade_point: schemas.TradePointCreate,
    db: Session = Depends(get_async_session)
):
    return await create_trade_point(db, trade_point)


# Получить торговую точку по ID
@router.get("/trade_points/{trade_point_id}",
            response_model=schemas.TradePoint)
async def read_trade_point_endpoint(
    trade_point_id: int,
    db: Session = Depends(get_async_session)
):
    trade_point = await get_trade_point(db, trade_point_id)
    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point


# Получить список всех торговых точек
@router.get("/trade_points/", response_model=list[schemas.TradePoint])
async def read_trade_points_endpoint(
    db: Session = Depends(get_async_session)
):
    return await get_trade_points(db)


# Обновить информацию о торговой точке
@router.put("/trade_points/{trade_point_id}",
            response_model=schemas.TradePoint)
async def update_trade_point_endpoint(
    trade_point_id: int,
    trade_point_data: schemas.TradePointUpdate,
    db: Session = Depends(get_async_session)
):
    trade_point = await update_trade_point(
        db,
        trade_point_id,
        trade_point_data)
    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point


# Удалить торговую точку
@router.delete("/trade_points/{trade_point_id}",
               response_model=schemas.TradePoint)
async def delete_trade_point_endpoint(
    trade_point_id: int,
    db: Session = Depends(get_async_session)
):
    trade_point = await delete_trade_point(db, trade_point_id)
    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point
