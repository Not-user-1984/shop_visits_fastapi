from pydantic import BaseModel
from enum import Enum
import datetime
from typing import Optional


# Схема для создания заказа
class OrderStatus(BaseModel):
    status: Enum
    trade_point_id: int


class OrderResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: str
    executor_id: Optional[int]
    created_at: datetime.datetime
