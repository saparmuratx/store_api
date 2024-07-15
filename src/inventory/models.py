from sqlalchemy import Column, String, Integer, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from src.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    opening_hours = Column(Time)

    user_id = Column(Integer, ForeignKey("users.id"))

    items = relationship("Item", back_populates="vendor")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    vendor = relationship("Vendor", back_populates="items")
