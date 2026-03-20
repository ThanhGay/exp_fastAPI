from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.repositories.catalog import product_repository as repo
from app.schemas.catalog.product import (
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    ProductView,
)
from app.schemas.common import BaseQueryParams


def get_all_products(db: Session, query: BaseQueryParams | None = None):
    params = query or BaseQueryParams()
    return repo.get_multi(
        db,
        limit=params.limit,
        offset=params.offset,
        keyword=params.keyword,
    )


def get_product_by_id(db: Session, id: int):
    if not repo.exist_product_id(db=db, id=id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    result = repo.get_by_id_with_category_name(db=db, id=id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    product, category_name = result

    return ProductView(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id,
        category_name=category_name,
    )


def create_product(product_in: ProductCreate, db: Session, user_id: int):
    print(f"Data create product: {product_in}")
    return repo.create(db=db, req=product_in, user_id=user_id)


def update_product(req: ProductUpdate, db: Session, user_id: int):
    print(f"Data update product: {req}")

    if not repo.exist_product_id(db=db, id=req.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return repo.update_product(db=db, req=req, user_id=user_id)


def soft_delete_product(req: ProductDelete, db: Session, user_id: int):
    print(f"Delete product id: {req.id}")

    if not repo.exist_product_id(db=db, id=req.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return repo.delete_product(db=db, id=req.id, user_id=user_id)


def remove_product(id: int, db: Session):
    print(f"Delete permanent product_id: {id}")
    return repo.remove_product(db=db, id=id)


def get_products_by_category_id(category_id: int, db: Session):
    results = repo.get_by_category_id_with_category_name(db=db, category_id=category_id)

    return [
        ProductView(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id,
            category_name=category_name,
        )
        for product, category_name in results
    ]
