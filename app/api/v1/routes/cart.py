from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id
from app.schemas.common import ApiResponse, BaseQueryParams
from app.schemas.ord.cart import CartItemView, CartItemCreate, CartItemDelete
from app.services.order import cart_service
from app.utils.response import ok

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/mine", response_model=ApiResponse[list[CartItemView]])
def get_my_cart(
    db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)
):
    items = cart_service.get_my_cart(db=db, user_id=current_id)
    return ok(data=items)


@router.post(
    "/add",
    response_model=ApiResponse[CartItemView],
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    req: CartItemCreate,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    new_item = cart_service.add_to_cart(db=db, user_id=current_id, req=req)
    return ok(data=new_item, message="Product added to your cast.")


@router.delete("/remove/{cart_id}")
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_id: int = Depends(get_current_user_id),
):
    request = CartItemDelete(id=cart_id)

    res = cart_service.delete_from_cart(db=db, user_id=current_id, req=request)
    return ok(data=res, message="Removed this product from your cart")
