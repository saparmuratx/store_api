from sqlalchemy import Column, String, Integer, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from src.database import Base


class Establishment(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    opening_hours = Column(Time)

    user_id = Column(Integer, ForeignKey("users.id"))

    items = relationship("Item", back_populates="establishment")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))

    establishment_id = Column(Integer, ForeignKey("establishments.id"))

    establishment = relationship("Establishment", back_populates="items")
