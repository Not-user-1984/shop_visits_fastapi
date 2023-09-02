from pydantic import BaseModel
from typing import List
from enum import Enum
import datetime

# Схема для создания заказа
class OrderCreate(BaseModel):
    phone_number: str
    trade_point_id: int


# Схема для ответа с информацией о заказе
class OrderResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: Enum
    created_at: datetime.datetime




# Схема для ответа с информацией о клиенте
class CustomerResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    # Другие поля клиента


# Схема для ответа со списком заказов клиента
class CustomerOrdersResponse(BaseModel):
    customer: CustomerResponse
    orders: List[OrderResponse]
