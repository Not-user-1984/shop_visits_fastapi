
import datetime
from pydantic import BaseModel


class WorkerBase(BaseModel):
    name: str
    phone_number: str
    trade_point_id: int


class WorkerCreate(WorkerBase):
    pass


class Worker(WorkerBase):
    id: int

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    phone_number: str
    trade_point_id: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class VisitBase(BaseModel):
    executor_id: int
    order_id: int
    author_id: int
    where_id: int


class VisitCreate(VisitBase):
    pass


class Visit(VisitBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class TradePointBase(BaseModel):
    name: str

class TradePointCreate(TradePointBase):
    pass


class TradePoint(TradePointBase):
    id: int

    class Config:
        orm_mode = True