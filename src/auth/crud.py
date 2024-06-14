from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

from psycopg2.errors import UniqueViolation

from src.auth import schemas, models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    user.password = hash_password(user.password)

    db_user = models.User(
        username=user.username, name=user.name, hashed_password=user.password
    )

    try:
        db.add(db_user)
        db.commit()

        db.refresh(db_user)
    except IntegrityError:
        raise KeyError("username is already in use")

    return db_user


def read_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def find_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
