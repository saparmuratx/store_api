from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, index=True, unique=True)

    name = Column(String)

    hashed_password = Column(String)

    created_date = Column(DateTime, default=datetime.now())

    active = Column(Boolean, default=True)

    establishments = relationship("Establishment", backref="establishment")

    items = relationship("Item", backref="item")
