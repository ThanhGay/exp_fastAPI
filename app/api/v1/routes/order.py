from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ord.order import OrderView, OrderCreateDirect, OrderCreateFromCart
from app.api.deps import get_db, get_current_user_id
from app.services.order import order_service

router = APIRouter(prefix="/order", tags=["order"])


@router.get("", response_model=list[OrderView])
def get_my_orders_route(
    db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)
):
    return order_service.get_my_orders(db=db, user_id=current_id)


@router.get("/{ord_id}", response_model=OrderView)
def get_detail_order_route(
    ord_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return order_service.get_order_detail(db=db, order_id=ord_id, user_id=current_id)


@router.post("/from-cart")
def create_order_from_cart_route(
    req: OrderCreateFromCart,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return order_service.create_order_from_cart(db=db, user_id=current_id, req=req)


@router.post("", response_model=OrderView)
def create_order_direct_route(
    req: OrderCreateDirect,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return order_service.create_order_direct(db=db, user_id=current_id, req=req)
