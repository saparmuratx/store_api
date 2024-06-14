from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from . import models, schemas, crud

from src.database import engine, get_db

models.Base.metadata.create_all(bind=engine)


auth_router = APIRouter()


@auth_router.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
