from sqlalchemy.orm import Session

from app.db.models.ord import Order, OrderItem, Cart
from app.schemas.ord.order import OrderItemCreate, OrderCreate, OrderStatusEnum


def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_items_by_order_id(db: Session, order_id: int) -> list[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def create_order(db: Session, req: OrderCreate, user_id: int) -> Order:
    order = Order(
        user_id=user_id,
        status=OrderStatusEnum.IDLE.value,
        note=req.note,
        created_by=user_id,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def create_order_item(db: Session, item: OrderItemCreate, user_id: int) -> OrderItem:
    order_item = OrderItem(
        order_id=item.order_id,
        product_id=item.prod_id,
        count=item.count,
        price=item.price_per_unit,
        created_by=user_id,
    )

    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return order_item
