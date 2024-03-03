from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import schemas, models


def read_establishment(db: Session, establishment_id):
    return (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )


def read_establishments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Establishment).offset(skip).limit(limit).all()


def create_establishment(db: Session, establishment: schemas.EstablishtmentCreate):
    db_establishment = models.Establishment(**establishment.model_dump())

    db.add(db_establishment)

    db.commit()
    db.refresh(db_establishment)

    return db_establishment


def update_establishment(
    db: Session, establishment: schemas.EstablishmentUpdate, establishment_id: int
) -> models.Establishment:
    db_establishment = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )

    if not db_establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    data = establishment.model_dump()

    for key, value in data.items():
        if value:
            setattr(db_establishment, key, value)

    db.commit()

    return db_establishment


def delete_establishment(db: Session, establishment_id: int):
    db_establishment = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )

    # items = db_establishment.items

    db.delete(db_establishment)
    db.commit()


def read_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def read_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate, establishment_id):
    db_item = models.Item(**item.model_dump(), establishment_id=establishment_id)

    db.add(db_item)

    db.commit()
    db.refresh(db_item)

    return db_item


def update_item(db: Session, item: schemas.ItemUpdate, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = item.model_dump()

    for key, value in data.items():
        if value:
            setattr(db_item, key, value)

    db.commit()

    return db_item


def delete_item(db: Session, item_id):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    db.delete(db_item)
    db.commit()
