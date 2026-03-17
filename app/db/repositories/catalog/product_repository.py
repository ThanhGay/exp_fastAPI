from app.schemas.catalog.product import ProductCreate, ProductUpdate, ProductView
from app.db.models.prod.models import Product, Category
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone


def get_multi(db: Session):
    res = db.query(Product).where(Product.is_deleted != True)
    
    return res.all()

def get_by_id(db: Session, id: int) -> Product | None:
    return db.query(Product).filter(Product.id == id, Product.is_deleted != True).first()

def get_by_id_with_category_name(db: Session, id: int) -> Product | None:
    return (
        db.query(Product, Category.name.label("category_name"))
        .outerjoin(Category, Product.category_id == Category.id)
        .filter(Product.id == id, Product.is_deleted != True)
        .first()
    )

def get_by_category_id_with_category_name(db: Session, category_id: int):
    return (
        db.query(Product, Category.name.label("category_name"))
        .outerjoin(Category, Product.category_id == Category.id)
        .filter(Product.category_id == category_id, Product.is_deleted != True)
        .all()
    )


def create(db: Session, req: ProductCreate, user_id: int) -> Product:
    product = Product(
        name=req.name,
        description=req.description,
        price=req.price,
        stock=req.stock,
        category_id=req.category_id,
        created_by=user_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(db: Session, req: ProductUpdate, user_id: int) -> Product:
    prod = get_by_id(db=db, id=req.id)
    if not prod:
        return None

    prod.name = req.name
    prod.description = req.description
    prod.price = req.price
    prod.stock = req.stock
    prod.category_id = req.category_id

    prod.modified_at = datetime.now(tz=timezone.utc)
    prod.modified_by = user_id

    db.commit()
    db.refresh(prod)

    return prod


def delete_product(db: Session, id: int, user_id: int) -> bool:
    prod = get_by_id(db=db, id=id)
    if not prod:
        return False

    prod.is_deleted = True
    prod.deleted_at = datetime.now(tz=timezone.utc)
    prod.deleted_by = user_id

    db.commit()
    db.refresh(prod)

    return True


def remove_product(db: Session, id: int) -> bool:
    prod = get_by_id(db=db, id=id)

    if not prod:
        return False

    db.delete(prod)
    db.commit()

    return True
