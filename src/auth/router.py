from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from . import models, schemas, crud

from src.database import engine, get_db

models.Base.metadata.create_all(bind=engine)


auth_router = APIRouter()


@auth_router.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user)

    except KeyError as err:
        raise HTTPException(status_code=400, detail=str(err))

    return db_user


@auth_router.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.read_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
