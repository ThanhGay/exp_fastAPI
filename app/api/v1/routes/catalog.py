from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.catalog.product import ProductCreate, ProductView
from app.services.catalog import product_service

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"]
)

@router.post("/products", response_model=ProductView)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return product_service.create_product(product_in=product, db=db)

@router.get("/products", response_model=list[ProductView])
def get_all_products_route(db: Session = Depends(get_db)):
    return product_service.get_all_products(db=db)