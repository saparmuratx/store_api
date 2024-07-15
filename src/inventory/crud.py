from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import schemas, models


no_permission_error = HTTPException(
    status_code=401,
    detail="You do not have permission to update this resource.",
)


def read_vendor(db: Session, vendor_id):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()


def read_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).offset(skip).limit(limit).all()


def create_vendor(db: Session, vendor: schemas.VendorCreate, user_id: int):
    db_vendor = models.Vendor(**vendor.model_dump(), user_id=user_id)

    db.add(db_vendor)

    db.commit()
    db.refresh(db_vendor)

    return db_vendor


def update_vendor(
    db: Session, vendor: schemas.VendorUpdate, vendor_id: int, user_id: int
) -> models.Vendor:
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if db_vendor.user_id != user_id:
        raise no_permission_error

    data = vendor.model_dump()

    for key, value in data.items():
        if value:
            setattr(db_vendor, key, value)

    db.commit()

    return db_vendor


def delete_vendor(db: Session, vendor_id: int):
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

    # items = db_vendor.items

    db.delete(db_vendor)
    db.commit()


def read_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def read_items(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Item)
        .filter(models.Item.vendor_id.is_not(None))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_item(db: Session, item: schemas.ItemCreate, vendor_id: int, user_id: int):
    db_item = models.Item(**item.model_dump(), vendor_id=vendor_id, user_id=user_id)

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
