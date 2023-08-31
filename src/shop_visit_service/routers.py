import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_async_session

from . import schemas
from .models import Worker

router = APIRouter()


@router.get("/trade_points/{phone_number}",
             response_model=list[schemas.TradePoint]
    )

def get_trade_points_by_phone(phone_number: str, db: Session = Depends(get_async_session)):
    worker = db.query(Worker).filter(Worker.phone_number == phone_number).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    trade_points = worker.trade_point
    return trade_points