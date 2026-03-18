from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id, get_query_params
from app.schemas.catalog.product import ProductCreate, ProductView, ProductUpdate
from app.schemas.common.query_params import BaseQueryParams
from app.schemas.catalog.category import (
    CategoryView,
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
)
from app.services.catalog import product_service, category_service

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.post("/products", response_model=ProductView)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_id=Depends(get_current_user_id),
):
    return product_service.create_product(product_in=product, db=db, user_id=current_id)


@router.get("/products", response_model=list[ProductView])
def get_all_products_route(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    return product_service.get_all_products(db=db, query=query)


@router.get("/products/{prod_id}", response_model=ProductView)
def get_by_product_id_route(
    prod_id: int,
    db: Session = Depends(get_db),
):
    return product_service.get_product_by_id(db=db, id=prod_id)


@router.put("/products/{prod_id}")
def update_product_route(
    prod_id: int,
    prod_in: ProductCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = ProductUpdate(id=prod_id, **prod_in.model_dump())
    return product_service.update_product(req=request, db=db, user_id=current_id)


@router.delete("/products/{prod_id}")
def delete_product_route(
    prod_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryDelete(id=prod_id)
    return product_service.soft_delete_product(db=db, req=request, user_id=current_id)


"""
=========================== CATEGORY ============================
"""


@router.get("", response_model=list[CategoryView])
def get_all_category_route(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    return category_service.get_all_categories(db=db, query=query)


@router.post("", response_model=CategoryView)
def create_category_route(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return category_service.create_category(db=db, req=category, user_id=current_id)


@router.put("/{category_id}", response_model=CategoryView)
def update_category_route(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryUpdate(id=category_id, **category.model_dump())
    return category_service.update_category(db=db, req=request, user_id=current_id)


@router.delete("/{category_id}")
def delete_category_route(
    category_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryDelete(id=category_id)
    return category_service.soft_delete_category(db=db, req=request, user_id=current_id)

@router.get("/{category_id}/products")
def get_products_by_category_route(category_id: int, db: Session=Depends(get_db)):
    return product_service.get_products_by_category_id(db=db, category_id=category_id)
