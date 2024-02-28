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
