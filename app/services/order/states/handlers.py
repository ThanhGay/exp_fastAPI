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


def _get_order_items(db: Session, order: Order):
    return order_repo.get_items_by_order_id(db=db, order_id=order.id)


def _get_products_map_for_items(db: Session, order_items):
    product_ids = list({item.product_id for item in order_items})
    products = prod_repo.get_by_ids(db=db, ids=product_ids)
    return {prod.id: prod for prod in products}


class ProcessingHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        order_items = _get_order_items(db=db, order=order)
        products_map = _get_products_map_for_items(db=db, order_items=order_items)
        for item in order_items:
            prod = products_map.get(item.product_id)
            if not prod or item.count <= 0 or prod.stock < item.count:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product_id={item.product_id}",
                )


class DeliveringHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        order_items = _get_order_items(db=db, order=order)
        products_map = _get_products_map_for_items(db=db, order_items=order_items)

        # Validate again before decreasing to avoid negative stock.
        for item in order_items:
            prod = products_map.get(item.product_id)
            if not prod or item.count <= 0 or prod.stock < item.count:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for product_id={item.product_id}",
                )

        for item in order_items:
            products_map[item.product_id].stock -= item.count


class DeliveredHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        # No stock side-effect at this point (stock-out already happened in DELIVERING).
        return None


class ReturnRequestedHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        # Waiting for admin decision; no stock update at request stage.
        return None


class DoneHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        return None


class RefundHandler(BaseHandler):
    def handle(self, db: Session, order: Order) -> None:
        # CANCEL happens after shipping when transitioning from DELIVERED -> CANCEL.
        # At this moment, `order.status` is still the OLD status (before order_repo.update_order_status()).
        if order.status != OrderStatusEnum.DELIVERED.value:
            return None

        order_items = _get_order_items(db=db, order=order)
        products_map = _get_products_map_for_items(db=db, order_items=order_items)
        for item in order_items:
            prod = products_map.get(item.product_id)
            if not prod or item.count <= 0:
                continue
            prod.stock += item.count
