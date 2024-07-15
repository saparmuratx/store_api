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
    vendor_id: int

    model_config = ConfigDict(from_attributes=True)


class ItemUpdate(ItemBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class VendorBase(BaseModel):
    name: str
    description: str
    location: str
    opening_hours: time


class VendorCreate(VendorBase):
    pass


class VendorCreateResponse(VendorBase):
    id: int
    user_id: int


class Vendor(VendorBase):
    id: int

    user_id: int
    items: list[Item] = []

    model_config = ConfigDict(from_attributes=True)


class VendorUpdate(VendorBase):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    opening_hours: time | None = None


class VendorUpdateResponse(VendorBase):
    id: int
