from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.services.order import cart_service
from app.schemas.order.cart import CartItemView, CartItemCreate, CartItemDelete

router = APIRouter(prefix="", tags=["cart"])


@router.get("/my-cart", response_model=list[CartItemView])
def get_my_cart(
    db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)
):
    return cart_service.get_my_cart(db=db, user_id=current_id)


@router.post("/add", response_model=CartItemView)
def add_to_cart(
    req: CartItemCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    return cart_service.add_to_cart(db=db, user_id=current_id, req=req)


@router.delete("/remove/{cart_id}")
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CartItemDelete(id=cart_id)

    res = cart_service.delete_from_cart(db=db, user_id=current_id, req=request)
    if res:
        return {"message": "Removed this product from your cart"}
