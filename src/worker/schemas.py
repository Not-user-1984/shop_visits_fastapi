import datetime

from typing import List

from pydantic import BaseModel


class WorkerBase(BaseModel):
    name: str
    phone_number: str
    trade_point_id: int


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(WorkerBase):
    pass


class WorkerResponse(WorkerBase):
    id: int


class WorkerListResponse(BaseModel):
    workers: List[WorkerResponse]


class WorkerPhoneNumber(BaseModel):
    phone_number: str
