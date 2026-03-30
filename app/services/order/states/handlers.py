from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.ord import Order
from app.db.repositories.catalog import product_repository as prod_repo
from app.db.repositories.order import order_repository as order_repo
from app.schemas.ord.order import OrderStatusEnum


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, db: Session, order: Order) -> None:
        raise NotImplementedError


class ProcessingHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        print(f"[Processing] Order #{order.id}")
        order_items = order_repo.get_items_by_order_id(db=db, order_id=order.id)
        for item in order_items:
            ok = prod_repo.validate_stock(db=db, id=item.product_id, count=item.count)
            if not ok:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product_id={item.product_id}",
                )


class DeliveringHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        print(f"[Delivering] Shipping order #{order.id}")
        order_items = order_repo.get_items_by_order_id(db=db, order_id=order.id)

        # Validate again before decreasing to avoid negative stock.
        for item in order_items:
            ok = prod_repo.validate_stock(db=db, id=item.product_id, count=item.count)
            if not ok:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product_id={item.product_id}",
                )

        for item in order_items:
            prod_repo.decrease_stock(db=db, id=item.product_id, count=item.count)


class DeliveredHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        print(f"[Delivered] Completed shipping order #{order.id}")
        # No stock side-effect at this point (stock-out already happened in DELIVERING).
        return


class DoneHandler(BaseHandler):
    def handle(self, db, order):
        print(f"[Done] Customer confirm receiving their order #{order.id}")
        return


class RefundHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        # CANCEL happens after shipping when transitioning from DELIVERED -> CANCEL.
        # At this moment, `order.status` is still the OLD status (before order_repo.update_order_status()).
        if order.status != OrderStatusEnum.DELIVERED.value:
            return

        order_items = order_repo.get_items_by_order_id(db=db, order_id=order.id)
        for item in order_items:
            prod_repo.increase_stock(db=db, id=item.product_id, count=item.count)
