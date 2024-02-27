from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas

from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/establishments/", response_model=schemas.Establishment)
def create_establishment(
    establishment: schemas.EstablishtmentCreate, db: Session = Depends(get_db)
):
    return crud.create_establishment(db=db, establishment=establishment)


@router.get("/establishments/{establishment_id}/", response_model=schemas.Establishment)
def get_establishment(establishment_id: int, db: Session = Depends(get_db)):
    establishment = crud.get_establishment(db=db, establishment_id=establishment_id)

    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    return establishment


@router.get("/establishments/", response_model=list[schemas.Establishment])
def read_establishmetns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_establishments(db=db, skip=skip, limit=limit)


@router.post("/establishments/{establishment_id}/items/", response_model=schemas.Item)
def create_item(
    establishment_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_item(db, item=item, establishment_id=establishment_id)


@router.get("/items/", response_model=list[schemas.Item])
def get_items(skip: int, limit: int, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)

    return items


@router.get("/items/{item_id}/", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)

    return item
