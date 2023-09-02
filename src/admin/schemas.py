from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    trade_point_id: int


class CustomerUpdate(CustomerCreate):
    pass
