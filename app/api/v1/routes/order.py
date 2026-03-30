from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.ord.order import (
    OrderView,
    OrderCreateDirect,
    OrderCreateFromCart,
    OrderUpdateStatus,
)
from app.api.deps import get_db, get_current_user_id
from app.services.order import order_service
from app.schemas.common.response import ApiResponse
from app.utils.response import ok

router = APIRouter(
    prefix="/order", tags=["order"], dependencies=[Depends(get_current_user_id)]
)


@router.get("", response_model=ApiResponse[list[OrderView]])
def get_my_orders_route(
    db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)
):
    items = order_service.get_my_orders(db=db, user_id=current_id)
    return ok(data=items)


@router.get("/{ord_id}", response_model=ApiResponse[OrderView])
def get_detail_order_route(
    ord_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    detail = order_service.get_order_detail(db=db, order_id=ord_id, user_id=current_id)
    return ok(data=detail)


@router.post(
    "/from-cart",
    response_model=ApiResponse[OrderView],
    status_code=status.HTTP_201_CREATED,
)
def create_order_from_cart_route(
    req: OrderCreateFromCart,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    created = order_service.create_order_from_cart(db=db, user_id=current_id, req=req)
    return ok(data=created, message="Order created")


@router.post(
    "",
    response_model=ApiResponse[OrderView],
    status_code=status.HTTP_201_CREATED,
)
def create_order_direct_route(
    req: OrderCreateDirect,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    created = order_service.create_order_direct(db=db, user_id=current_id, req=req)
    return ok(data=created, message="Order created")


@router.patch("/{ord_id}/status")
def update_status_order(
    ord_id: int,
    req: OrderUpdateStatus,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):

    order_service.update_order_status(
        db=db, user_id=current_id, order_id=ord_id, new_status=req.status
    )

    return ok(message=f"Don hang #{ord_id} cua ban da duoc cap nhat trang thai.")
