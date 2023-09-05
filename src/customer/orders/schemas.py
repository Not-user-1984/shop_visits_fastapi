from pydantic import BaseModel
from typing import List
from enum import Enum
import datetime
from typing import Optional


# Схема для создания заказа
class OrderCreate(BaseModel):
    phone_number: str
    trade_point_id: int



class OrderDelete(BaseModel):
    phone_number: str


# Схема для ответа с информацией о заказе
class OrderResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: Enum
    executor_id: Optional[int]
    created_at: datetime.datetime


# Схема для ответа с информацией о клиенте
class CustomerResponse(BaseModel):
    id: int
    name: str
    phone_number: str


# Схема для ответа со списком заказов клиента
class CustomerOrdersResponse(BaseModel):
    customer: CustomerResponse
    orders: List[OrderResponse]


# Схема для ответа с информацией о визите
class VisitResponse(BaseModel):
    created_at: datetime.datetime
    executor_id: int
    order_id: int
    author_id: int
    where_id: int
