from app.schemas.ord.cart import CartItemCreate
from app.db.models.ord import Cart
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timezone


def get_cart_by_user_id(db: Session, user_id: int):
    return (
        db.query(Cart)
        .filter(Cart.is_deleted != True, Cart.user_id == user_id)
        .order_by(Cart.created_at.desc())
        .all()
    )


def get_by_id(db: Session, id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.id == id, Cart.is_deleted != True).first()


def get_by_ids_and_user(db: Session, ids: list[int], user_id: int) -> list[Cart]:
    if not ids:
        return []
    return (
        db.query(Cart)
        .filter(Cart.id.in_(ids), Cart.user_id == user_id, Cart.is_deleted != True)
        .all()
    )


def create(db: Session, req: CartItemCreate, user_id: int) -> Cart:
    cart_item = Cart(
        user_id=user_id,
        product_id=req.product_id,
        count=req.count,
        created_by=user_id,
    )

    db.add(cart_item)
    db.flush()

    return cart_item


def soft_delete_by_id(db: Session, id: int, user_id: int) -> bool:
    cart_item = get_by_id(db=db, id=id)
    if not cart_item:
        return False

    cart_item.is_deleted = True
    cart_item.deleted_at = datetime.now(tz=timezone.utc)
    cart_item.deleted_by = user_id

    db.flush()

    return True


def soft_delete_by_ids(db: Session, ids: list[int], user_id: int) -> int:
    if not ids:
        return 0
    now = datetime.now(tz=timezone.utc)
    updated = (
        db.query(Cart)
        .filter(Cart.id.in_(ids), Cart.user_id == user_id, Cart.is_deleted != True)
        .update(
            {
                Cart.is_deleted: True,
                Cart.deleted_at: now,
                Cart.deleted_by: user_id,
            },
            synchronize_session=False,
        )
    )
    db.flush()
    return updated


def remove_cart_item(db: Session, id: int) -> bool:
    cart_item = get_by_id(db=db, id=id)

    if not cart_item:
        return False

    db.delete(cart_item)
    db.flush()

    return True


def exist_cart_with_product_id_and_user_id(
    db: Session, user_id: int, product_id
) -> bool:
    return (
        db.query(Cart)
        .filter(
            Cart.product_id == product_id,
            Cart.user_id == user_id,
            Cart.is_deleted != True,
        )
        .first()
    )


def add_more(db: Session, item: Cart, count: int, user_id: int) -> Cart:
    item.count += count

    item.modified_at = datetime.now(tz=timezone.utc)
    item.modified_by = user_id

    db.flush()

    return item
