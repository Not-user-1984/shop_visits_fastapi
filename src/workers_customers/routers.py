from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_async_session
from .crud import (
    create_worker,
    get_workers,
    create_customer,
    create_visit,
    get_visits,
    get_trade_points_by_worker_phone,
    get_customers
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


# Маршруты для сотрудников
@router.post("/workers/", response_model=schemas.Worker)
async def create_worker_endpoint(
    worker_data: schemas.WorkerCreate,
    db: Session = Depends(get_async_session)
):
    worker = await create_worker(db, worker_data)
    return worker


@router.get("/workers/", response_model=list[schemas.Worker])
async def get_workers_endpoint(
    db: Session = Depends(get_async_session)
):
    workers = await get_workers(db)
    return workers


# Маршруты для заказчиков
@router.post("/customers/", response_model=schemas.Customer)
async def create_customer_endpoint(
    customer_data: schemas.CustomerCreate,
    db: Session = Depends(get_async_session)
):
    customer = await create_customer(db, customer_data)
    return customer


@router.get("/customers/", response_model=list[schemas.Customer])
async def get_customers_endpoint(
    db: Session = Depends(get_async_session)
):
    customers = await get_customers(db)
    return customers


# Маршруты для посещений
@router.post("/visits/", response_model=schemas.Visit)
async def create_visit_endpoint(
    visit_data: schemas.VisitCreate,
    db: Session = Depends(get_async_session)
):
    visit = await create_visit(db, visit_data)
    return visit


@router.get("/visits/", response_model=list[schemas.Visit])
async def get_visits_endpoint(
    db: Session = Depends(get_async_session)
):
    visits = await get_visits(db)
    return visits
