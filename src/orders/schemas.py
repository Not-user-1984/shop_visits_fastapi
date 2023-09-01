from typing import Optional
from enum import Enum
import datetime
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'


class OrderGetBase(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: Enum
    executor_id: int
    created_at: datetime.datetime


class OrderCreate(OrderGetBase):
    pass


class Order(BaseModel):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

    @property
    def status_str(self):
        return self.status.value

class OrderPut(BaseModel):
    id: int
    status: Optional[OrderStatus]
