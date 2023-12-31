from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session

from trade_points import crud
from . import schemas

router = APIRouter()


# Создать торговую точку
@router.post("/trade_points/", response_model=schemas.TradePoint)
async def create_trade_point_endpoint(
    trade_point: schemas.TradePointCreate,
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.create_trade_point(db, trade_point)


# Получить торговую точку по ID
@router.get("/trade_points/{trade_point_id}",
            response_model=schemas.TradePoint)
async def read_trade_point_endpoint(
    trade_point_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    trade_point = await crud.get_trade_point(db, trade_point_id)
    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point


# Получить список всех торговых точек
@router.get("/trade_points/", response_model=list[schemas.TradePoint])
async def read_trade_points_endpoint(
    db: AsyncSession = Depends(get_async_session)
):
    return await crud.get_trade_points(db)


# Обновить информацию о торговой точке
@router.put("/trade_points/{trade_point_id}",
            response_model=schemas.TradePoint)
async def update_trade_point_endpoint(
    trade_point_id: int,
    trade_point_data: schemas.TradePointUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    trade_point = await crud.update_trade_point(
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
    db: AsyncSession = Depends(get_async_session)
):
    trade_point = await crud.delete_trade_point(db, trade_point_id)
    if not trade_point:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point
