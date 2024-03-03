from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(ItemBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class EstablishmentBase(BaseModel):
    name: str
    description: str
    location: str
    opening_hours: time


class EstablishtmentCreate(EstablishmentBase):
    pass


class EstablishmentCreateResponse(EstablishmentBase):
    id: int


class Establishment(EstablishmentBase):
    id: int

    items: list[Item] = []

    model_config = ConfigDict(from_attributes=True)


class EstablishmentUpdate(EstablishmentBase):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    opening_hours: time | None = None


class EstablishmentUpdateResponse(EstablishmentBase):
    id: int
