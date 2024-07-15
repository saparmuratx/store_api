from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import schemas, models


no_permission_error = HTTPException(
    status_code=401,
    detail="You do not have permission to update this resource.",
)


def read_establishment(db: Session, establishment_id):
    return (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )


def read_establishments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Establishment).offset(skip).limit(limit).all()


def create_establishment(
    db: Session, establishment: schemas.EstablishmentCreate, user_id: int
):
    db_establishment = models.Establishment(
        **establishment.model_dump(), user_id=user_id
    )

    db.add(db_establishment)

    db.commit()
    db.refresh(db_establishment)

    return db_establishment


def update_establishment(
    db: Session,
    establishment: schemas.EstablishmentUpdate,
    establishment_id: int,
    user_id: int,
) -> models.Establishment:
    db_establishment = (
        db.query(models.Establishment)
        .filter(models.Establishment.id == establishment_id)
        .first()
    )

    if not db_establishment:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if db_establishment.user_id != user_id:
        raise no_permission_error

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
    return (
        db.query(models.Item)
        .filter(models.Item.establishment_id.is_not(None))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(
    db: Session, item: schemas.ItemCreate, establishment_id: int, user_id: int
):
    db_item = models.Item(
        **item.model_dump(), establishment_id=establishment_id, user_id=user_id
    )

    db.add(db_item)

    db.commit()
    db.refresh(db_item)

    return db_item


def update_item(db: Session, item: schemas.ItemUpdate, item_id: int, user_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.user_id != user_id:
        raise no_permission_error

    data = item.model_dump()

    for key, value in data.items():
        if value:
            setattr(db_item, key, value)

    db.commit()

    return db_item


def delete_item(db: Session, item_id: int, user_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if db_item.user_id != user_id:
        raise no_permission_error

    db.delete(db_item)
    db.commit()
