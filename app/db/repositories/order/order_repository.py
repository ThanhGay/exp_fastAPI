from sqlalchemy.orm import Session

from app.db.models.ord import Order, OrderItem
from app.schemas.ord.order import OrderItemCreate, OrderCreate, OrderStatusEnum
from datetime import datetime, timezone


def get_orders_by_user(db: Session, user_id: int, status: str = None) -> list[Order]:
    stmt = db.query(Order).filter(Order.user_id == user_id, Order.is_deleted != True)

    if status is not None:
        stmt = stmt.filter(Order.status == status)

    return stmt.order_by(Order.created_at.desc()).all()


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_items_by_order_id(db: Session, order_id: int) -> list[OrderItem]:
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


def get_items_by_order_ids(db: Session, order_ids: list[int]) -> list[OrderItem]:
    if not order_ids:
        return []
    return db.query(OrderItem).filter(OrderItem.order_id.in_(order_ids)).all()


def create_order(db: Session, req: OrderCreate, user_id: int) -> Order:
    order = Order(
        user_id=user_id,
        status=OrderStatusEnum.IDLE.value,
        note=req.note,
        created_by=user_id,
    )

    db.add(order)
    db.flush()

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
    db.flush()

    return order_item


def update_order_status(db: Session, order: Order, status: str, user_id: int):
    order.status = status
    order.modified_by = user_id
    order.modified_at = datetime.now(tz=timezone.utc)

    db.flush()
