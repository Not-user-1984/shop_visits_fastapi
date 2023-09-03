from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import get_async_session

from worker import crud, schemas

router = APIRouter()

# создать работника
@router.post("/workers/",
             response_model=schemas.WorkerResponse)
async def create_worker(worker: schemas.WorkerCreate,
                        db: AsyncSession = Depends(get_async_session)):
    return await crud.create_worker(db, worker)


# посмотреть заказы на точки
@router.get("/workers/orders/",
            response_model=List[schemas.OrderResponse])
async def get_worker_orders(
    phone_number: str,
    db: AsyncSession = Depends(get_async_session)
):
    orders = await crud.get_tradepoint_orders(db, phone_number)

    return orders


# выбрать заказ на выполение
@router.post("/assign-order/{order_id}",
             response_model=schemas.OrderWorkerResponse)
async def assign_order(
    phone_number: str,
    order_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    order = await crud.assign_order_to_worker(db, phone_number, order_id)
    return order
   

@router.get("/workers/{worker_id}", response_model=schemas.WorkerResponse)
async def read_worker(worker_id: int, db: AsyncSession = Depends(get_async_session)):
    db_worker = crud.get_worker(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@router.get("/workers/", response_model=schemas.WorkerListResponse)
async def read_workers(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    workers = crud.get_workers(db, skip, limit)
    return {"workers": workers}

@router.put("/workers/{worker_id}", response_model=schemas.WorkerResponse)
async def update_worker(worker_id: int, worker: schemas.WorkerUpdate, db: AsyncSession = Depends(get_async_session)):
    db_worker = crud.update_worker(db, worker_id, worker)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@router.delete("/workers/{worker_id}", response_model=schemas.WorkerResponse)
async def delete_worker(worker_id: int, db: AsyncSession = Depends(get_async_session)):
    db_worker = crud.delete_worker(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
