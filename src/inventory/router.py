from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas

from src.database import get_db, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/establishments/", response_model=schemas.EstablishmentCreateResponse)
def create_establishment(
    establishment: schemas.EstablishtmentCreate, db: Session = Depends(get_db)
):
    return crud.create_establishment(db=db, establishment=establishment)


@router.get("/establishments/{establishment_id}/", response_model=schemas.Establishment)
def get_establishment(establishment_id: int, db: Session = Depends(get_db)):
    establishment = crud.read_establishment(db=db, establishment_id=establishment_id)

    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    return establishment


@router.get("/establishments/", response_model=list[schemas.Establishment])
def read_establishmetns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_establishments(db=db, skip=skip, limit=limit)


@router.put(
    "/establishments/{establishment_id}/",
    response_model=schemas.EstablishmentUpdateResponse,
)
def update_establishment(
    establishment_id: int,
    establishment: schemas.EstablishmentUpdate,
    db: Session = Depends(get_db),
):
    establishment = crud.update_establishment(db, establishment, establishment_id)

    return establishment


@router.delete("/establishments/{establishment_id}/", status_code=204)
def delete_establishment(establishment_id: int, db: Session = Depends(get_db)):
    establishment = crud.read_establishment(db, establishment_id)

    if not establishment:
        raise HTTPException(status_code=404, detail="Item not found")

    crud.delete_establishment(db, establishment_id)

    return None


@router.post("/establishments/{establishment_id}/items/", response_model=schemas.Item)
def create_item(
    establishment_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    establishment = crud.read_establishment(db, establishment_id)

    if not establishment:
        raise HTTPException(
            status_code=404,
            detail=f"Establishment not found with ID {establishment_id}",
        )

    return crud.create_item(db, item=item, establishment_id=establishment_id)


@router.get("/items/", response_model=list[schemas.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.read_items(db, skip=skip, limit=limit)

    return items


@router.get("/items/{item_id}/", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.read_item(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/items/{item_id}/", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_item(db, item, item_id)

    return updated_item


@router.delete("/items/{item_id}/", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.read_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    crud.delete_item(db, item_id)

    return None
