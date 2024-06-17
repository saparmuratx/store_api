from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas

from src.auth.schemas import User
from src.auth.router import get_current_active_user

from src.database import get_db, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/vendors/", response_model=schemas.EstablishmentCreateResponse)
def create_vendor(
    establishment: schemas.EstablishmentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return crud.create_establishment(
        db=db, establishment=establishment, user_id=current_user.id
    )


@router.get("/vendors/{vendor_id}/", response_model=schemas.Establishment)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    establishment = crud.read_establishment(db=db, establishment_id=vendor_id)

    if not establishment:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return establishment


@router.get("/vendors/", response_model=list[schemas.Establishment])
def read_establishmetns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_establishments(db=db, skip=skip, limit=limit)


@router.put(
    "/vendors/{vendor_id}/",
    response_model=schemas.EstablishmentUpdateResponse,
)
def update_vendor(
    vendor_id: int,
    establishment: schemas.EstablishmentUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    establishment = crud.update_establishment(
        db, establishment, vendor_id, current_user.id
    )

    return establishment


@router.delete("/vendors/{vendor_id}/", status_code=204)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    establishment = crud.read_establishment(db, vendor_id)

    if not establishment:
        raise HTTPException(status_code=404, detail="Item not found")

    crud.delete_establishment(db, vendor_id)

    return None


@router.post("/vendors/{vendor_id}/items/", response_model=schemas.Item)
def create_item(
    vendor_id: int,
    item: schemas.ItemCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    establishment = crud.read_establishment(db, vendor_id)

    if not establishment:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor not found with ID {vendor_id}",
        )

    if establishment.user_id != current_user.id:
        raise crud.no_permission_error

    return crud.create_item(
        db, item=item, establishment_id=vendor_id, user_id=current_user.id
    )


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
def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    updated_item = crud.update_item(db, item, item_id, current_user.id)

    return updated_item


@router.delete("/items/{item_id}/", status_code=204)
def delete_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    item = crud.read_item(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    crud.delete_item(db, item_id, current_user.id)

    return None
