from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.repositories.order import cart_repository as cart_repo
from app.db.repositories.catalog import product_repository as prod_repo
from app.schemas.ord.cart import CartItemView, CartItemCreate, CartItemDelete


def get_my_cart(db: Session, user_id: int):
    cart_items = cart_repo.get_cart_by_user_id(db=db, user_id=user_id)

    product_ids = {item.product_id for item in cart_items}
    products = prod_repo.get_by_ids(db=db, ids=list(product_ids))
    products_map = {p.id: p for p in products}

    return [
        CartItemView(
            id=item.id,
            product_id=item.product_id,
            price_per_unit=products_map[item.product_id].price,
            product_name=products_map[item.product_id].name,
            count=item.count,
        )
        for item in cart_items
        if item.product_id in products_map
    ]


def add_to_cart(db: Session, user_id: int, req: CartItemCreate):
    print(f"Data add to cart: {req}")

    if not prod_repo.exist_product_id(db=db, id=req.product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    exist_cart_item = cart_repo.exist_cart_with_product_id_and_user_id(
        db=db, user_id=user_id, product_id=req.product_id
    )
    if exist_cart_item:
        return cart_repo.add_more(
            db=db, item=exist_cart_item, count=req.count, user_id=user_id
        )
    return cart_repo.create(db=db, req=req, user_id=user_id)


def delete_from_cart(db: Session, user_id: int, req: CartItemDelete):
    print(f"Delete cart_id: {req.id}")

    cart_item = cart_repo.get_by_id(db=db, id=req.id)

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found cart item with id {req.id} or it be deleted",
        )

    if cart_item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to remove this",
        )

    return cart_repo.delete_cart_item(db=db, id=req.id, user_id=user_id)
