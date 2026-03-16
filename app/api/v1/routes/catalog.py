from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.catalog.product import ProductCreate, ProductView
from app.schemas.catalog.category import CategoryView, CategoryCreate, CategoryUpdate, CategoryDelete
from app.services.catalog import product_service, category_service

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

@router.get("/", response_model=list[CategoryView])
def get_all_category_route(db: Session=Depends(get_db)):
    return category_service.get_all_categories(db=db)

@router.post("/", response_model=CategoryView)
def create_category_route(category: CategoryCreate,db: Session = Depends(get_db),  current_id: int = Depends(get_current_user_id)):
    return category_service.create_category(db=db, req=category, user_id=current_id)

@router.put("/{category_id}", response_model=CategoryView)
def update_category_route(category_id: int, category: CategoryCreate, db: Session=Depends(get_db),  current_id: int = Depends(get_current_user_id)):
    request = CategoryUpdate(id=category_id, **category.model_dump())
    return category_service.update_category(db, request, current_id)

@router.delete("/{category_id}")
def delete_category_route(category_id: int, db: Session = Depends(get_db), current_id: int  = Depends(get_current_user_id)):
    request = CategoryDelete(id=category_id)
    return category_service.soft_delete_category(db, request, current_id)