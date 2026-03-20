from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id, get_query_params
from app.schemas.catalog.product import ProductCreate, ProductView, ProductUpdate
from app.schemas.common import BaseQueryParams, ApiResponse
from app.schemas.catalog.category import (
    CategoryView,
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
)
from app.services.catalog import product_service, category_service
from app.utils.response import ok

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.post(
    "/products",
    response_model=ApiResponse[ProductView],
    status_code=status.HTTP_201_CREATED,
)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_id=Depends(get_current_user_id),
):
    prod = product_service.create_product(product_in=product, db=db, user_id=current_id)
    return ok(data=prod, message="Product created")


@router.get("/products", response_model=ApiResponse[list[ProductView]])
def get_all_products_route(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    items = product_service.get_all_products(db=db, query=query)
    return ok(data=items)


@router.get("/products/{prod_id}", response_model=ApiResponse[ProductView])
def get_by_product_id_route(
    prod_id: int,
    db: Session = Depends(get_db),
):
    item = product_service.get_product_by_id(db=db, id=prod_id)

    return ok(data=item)


@router.put("/products/{prod_id}", response_model=ApiResponse[ProductView])
def update_product_route(
    prod_id: int,
    prod_in: ProductCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = ProductUpdate(id=prod_id, **prod_in.model_dump())
    updated = product_service.update_product(req=request, db=db, user_id=current_id)

    return ok(data=updated, message="Product updated")


@router.delete("/products/{prod_id}", response_model=ApiResponse[bool])
def delete_product_route(
    prod_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryDelete(id=prod_id)
    deleted = product_service.soft_delete_product(
        db=db, req=request, user_id=current_id
    )

    return ok(data=deleted, message="Product deleted")


"""
=========================== CATEGORY ============================
"""


@router.get("", response_model=ApiResponse[list[CategoryView]])
def get_all_category_route(
    db: Session = Depends(get_db),
    query: BaseQueryParams = Depends(get_query_params),
):
    items = category_service.get_all_categories(db=db, query=query)
    return ok(data=items)


@router.post(
    "",
    response_model=ApiResponse[CategoryView],
    status_code=status.HTTP_201_CREATED,
)
def create_category_route(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    created = category_service.create_category(db=db, req=category, user_id=current_id)

    return ok(data=created, message="Category created")


@router.put("/{category_id}", response_model=ApiResponse[CategoryView])
def update_category_route(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryUpdate(id=category_id, **category.model_dump())
    updated = category_service.update_category(db=db, req=request, user_id=current_id)

    return ok(data=updated, message="Category updated")


@router.delete("/{category_id}", response_model=ApiResponse[bool])
def delete_category_route(
    category_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CategoryDelete(id=category_id)
    deleted = category_service.soft_delete_category(
        db=db, req=request, user_id=current_id
    )

    return ok(data=deleted, message="Category deleted")


@router.get(
    "/{category_id}/products",
    response_model=ApiResponse[list[ProductView]],
)
def get_products_by_category_route(category_id: int, db: Session = Depends(get_db)):
    data = product_service.get_products_by_category_id(db=db, category_id=category_id)
    return ok(data=data)
