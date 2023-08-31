import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_async_session

from .models import Customer, TradePoint, Visit, Worker

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


@router.post("/trade_points/", response_model=schemas.TradePoint)
def create_trade_point(trade_point: schemas.TradePointCreate, db: Session = Depends(get_db)):
    db_trade_point = TradePoint(**trade_point.dict())
    db.add(db_trade_point)
    db.commit()
    db.refresh(db_trade_point)
    return db_trade_point


@router.get("/trade_points/{trade_point_id}", response_model=schemas.TradePoint)
def read_trade_point(trade_point_id: int, db: Session = Depends(get_db)):
    trade_point = db.query(TradePoint).filter(TradePoint.id == trade_point_id).first()
    if trade_point is None:
        raise HTTPException(status_code=404, detail="Trade Point not found")
    return trade_point

# Операции CRUD для Worker

@router.post("/workers/", response_model=schemas.Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.get("/workers/{worker_id}", response_model=schemas.Worker)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

# Операции CRUD для Customer

@router.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Операции CRUD для Order

@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Операции CRUD для Visit

@router.post("/visits/", response_model=schemas.Visit)
def create_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):
    db_visit = Visit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

@router.get("/visits/{visit_id}", response_model=schemas.Visit)
def read_visit(visit_id: int, db: Session = Depends(get_db)):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit
