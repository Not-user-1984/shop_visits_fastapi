from pydantic import BaseModel
from typing import List
from enum import Enum
import datetime
from typing import Optional


class OrderCreate(BaseModel):
    phone_number: str
    trade_point_id: int


class OrderDelete(BaseModel):
    phone_number: str


class OrderResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: Enum
    executor_id: Optional[int]
    created_at: datetime.datetime


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone_number: str


class CustomerOrdersResponse(BaseModel):
    customer: CustomerResponse
    orders: List[OrderResponse]


class VisitResponse(BaseModel):
    created_at: datetime.datetime
    executor_id: int
    order_id: int
    author_id: int
    where_id: int
