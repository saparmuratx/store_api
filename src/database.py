from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base:
    __allow_unmapped__ = True


Base = declarative_base(cls=Base)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
