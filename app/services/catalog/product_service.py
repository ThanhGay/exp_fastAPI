from sqlalchemy.orm import Session
from app.db.repositories.catalog import product_repository as repo
from app.schemas.catalog.product import ProductCreate 

def get_all_products(db: Session):
    return repo.get_multi(db)

def create_product(product_in: ProductCreate, db: Session):
    print(f"Data create product: {product_in}")
    return repo.create(db, product_in)
