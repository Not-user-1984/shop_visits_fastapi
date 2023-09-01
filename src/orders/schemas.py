
from enum import Enum
import datetime
from pydantic import BaseModel


class OrderStatus(str, Enum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'


class OrderBase(BaseModel):
    where_id: int
    author_id: int
    status: OrderStatus
    executor_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    created_at: datetime.datetime
    ended_at: datetime.datetime

    class Config:
        orm_mode = True
