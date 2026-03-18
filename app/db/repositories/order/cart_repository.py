from app.schemas.ord.cart import CartItemCreate
from app.db.models.ord import Cart
from sqlalchemy.orm import Session
from datetime import datetime, timezone


def get_cart_by_user_id(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.is_deleted != True, Cart.user_id == user_id).all()


def get_by_id(db: Session, id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.id == id, Cart.is_deleted != True).first()


def create(db: Session, req: CartItemCreate, user_id: int) -> Cart:
    cart_item = Cart(
        user_id=user_id,
        product_id=req.product_id,
        count=req.count,
        created_by=user_id,
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def delete_cart_item(db: Session, id: int, user_id: int) -> bool:
    cart_item = get_by_id(db=db, id=id)
    if not cart_item:
        return False

    cart_item.is_deleted = True
    cart_item.deleted_at = datetime.now(tz=timezone.utc)
    cart_item.deleted_by = user_id

    db.commit()
    db.refresh(cart_item)

    return True


def remove_cart_item(db: Session, id: int) -> bool:
    cart_item = get_by_id(db=db, id=id)

    if not cart_item:
        return False

    db.delete(cart_item)
    db.commit()

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

    db.commit()
    db.refresh(item)

    return item
