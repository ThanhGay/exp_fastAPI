from sqlalchemy.orm import Session
from app.db.repositories.catalog import product_repository as repo
from app.schemas.catalog.product import (
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    ProductView,
)


def get_all_products(db: Session):
    return repo.get_multi(db)


def get_product_by_id(db: Session, id: int):
    result = repo.get_by_id_with_category_name(db=db, id=id)

    if not result:
        return None
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
    return repo.update_product(db=db, req=req, user_id=user_id)


def soft_delete_product(req: ProductDelete, db: Session, user_id: int):
    print(f"Delete product id: {req.id}")
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
