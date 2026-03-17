from app.schemas.catalog.product import ProductCreate
from app.models.prod.models import Product
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_multi(db: Session):
    res = db.query(Product).where(Product.is_deleted != True)
    print(f"query: {res}")
    return res.all()

def create(db: Session, product_in: ProductCreate) -> Product:
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
    