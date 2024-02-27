from pydantic import BaseModel
from datetime import time


class ItemBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    establishment_id: int

    class Config:
        orm_mode = True


class EstablishmentBase(BaseModel):
    name: str
    description: str
    location: str
    opening_hours: time


class EstablishtmentCreate(EstablishmentBase):
    pass


class Establishment(EstablishmentBase):
    id: int

    items: list[Item] = []

    class Config:
        orm_mode = True
