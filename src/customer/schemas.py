from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone_number: str


class CustomerResponse(CustomerCreate):
    id: int


class CustomerUpdate(CustomerCreate):
    pass
