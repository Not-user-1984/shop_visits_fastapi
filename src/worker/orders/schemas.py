import datetime
from enum import Enum

from typing import Optional
from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: Enum
    created_at: datetime.datetime
    ended_at: datetime.datetime


class OrderWorkerResponse(BaseModel):
    id: int
    where_id: int
    author_id: int
    status: str
    executor_id: int
    created_at: datetime.datetime
    ended_at: datetime.datetime
    executor_id: Optional[int]
