from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from worker import crud, schemas ,utils

router = APIRouter()


# создать работника
@router.post("/workers/",
             response_model=schemas.WorkerResponse)
async def create_worker(worker: schemas.WorkerCreate,
                        db: AsyncSession = Depends(get_async_session)):
    cleaned_phone_number = await utils.validate_phone_number(
        worker.phone_number, db)
    return await crud.create_worker(db, worker, cleaned_phone_number)


@router.get("/worker/{phone_number}/",
            response_model=schemas.WorkerResponse)
async def read_worker(
    phone_number: str,
    db: AsyncSession = Depends(get_async_session)
):
    db_worker = await crud.get_worker(db, phone_number)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.get("/workers/",
            response_model=schemas.WorkerListResponse)
async def read_workers(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):
    workers = await crud.get_workers(db, skip, limit)
    return {"workers": workers}


@router.put("/workers/{worker_id}",
            response_model=schemas.WorkerResponse)
async def update_worker(
    worker_id: int,
    worker: schemas.WorkerUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    db_worker = crud.update_worker(db, worker_id, worker)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.delete("/workers/{worker_id}",
            response_model=schemas.WorkerResponse)
async def delete_worker(worker_id: int, db: AsyncSession = Depends(get_async_session)):
    db_worker = await crud.delete_worker(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
