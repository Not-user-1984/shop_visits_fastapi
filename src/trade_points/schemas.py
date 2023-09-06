from pydantic import BaseModel


class TradePointBase(BaseModel):
    name: str


class TradePointCreate(TradePointBase):
    pass


class TradePoint(TradePointBase):
    id: int

    class Config:
        orm_mode = True


class TradePointUpdate(TradePointBase):
    name: str
