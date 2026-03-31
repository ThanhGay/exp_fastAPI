from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.order import order_repository as order_repo
from app.db.repositories.order import cart_repository as cart_repo
from app.db.repositories.catalog import product_repository as prod_repo
from app.schemas.ord.order import (
    OrderCreate,
    OrderCreateDirect,
    OrderCreateFromCart,
    OrderQueryParams,
    OrderView,
    OrderItemCreate,
    OrderItemView,
    OrderStatusEnum,
    OrderStatus,
)

from app.services.order.states.transition import TRANSITIONS
from app.services.order.states.registry import HANDLERS


def create_order_from_cart(db: Session, user_id: int, req: OrderCreateFromCart):
    """
    Create an order from selected cart item ids.
    """
    # Batch load all requested cart items for current user.
    valid_cart_items = cart_repo.get_by_ids_and_user(
        db=db, ids=req.item_ids, user_id=user_id
    )
    if len(valid_cart_items) != len(req.item_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some cart items not found or inaccessible",
        )

    if not valid_cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid cart items to create order",
        )

    # Lấy thông tin product để tính giá tại thời điểm tạo đơn
    product_ids = {item.product_id for item in valid_cart_items}
    products = prod_repo.get_by_ids(db=db, ids=list(product_ids))
    products_map = {p.id: p for p in products}

    missing_products = [pid for pid in product_ids if pid not in products_map]
    if missing_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Some products not found: {missing_products}",
        )

    # Tạo order + order items + dọn cart trong 1 transaction boundary.
    order_items: list[OrderItemView] = []
    total_price = 0.0
    try:
        order_req = OrderCreate(
            user_id=user_id,
            status=OrderStatusEnum.IDLE.value,
            note=None,
        )
        order = order_repo.create_order(db=db, req=order_req, user_id=user_id)

        for cart_item in valid_cart_items:
            product = products_map[cart_item.product_id]
            order_item_req = OrderItemCreate(
                order_id=order.id,
                prod_id=product.id,
                price_per_unit=product.price,
                count=cart_item.count,
            )
            created_item = order_repo.create_order_item(
                db=db, item=order_item_req, user_id=user_id
            )

            item_view = OrderItemView(
                id=created_item.id,
                prod_id=product.id,
                prod_name=product.name,
                price_per_unit=created_item.price,
                count=created_item.count,
            )
            order_items.append(item_view)
            total_price += created_item.price * created_item.count

        # Batch soft-delete selected cart rows after all order items created.
        cart_ids = [item.id for item in valid_cart_items]
        deleted_count = cart_repo.soft_delete_by_ids(
            db=db, ids=cart_ids, user_id=user_id
        )

        # Kiem tra so dong da xoa co chinh xac voi so luong products tao don
        if deleted_count != len(cart_ids):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to finalize cart cleanup for this order",
            )

        db.commit()
    except Exception:
        db.rollback()
        raise

    return OrderView(
        ord_id=order.id,
        user_id=order.user_id,
        status=order.status,
        status_str=OrderStatus[order.status],
        note=order.note,
        total_price=total_price,
        items=order_items,
    )


def create_order_direct(db: Session, user_id: int, req: OrderCreateDirect):
    valid_prod = prod_repo.get_by_id(db=db, id=req.item.prod_id)

    if not valid_prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found product_id: {req.item.prod_id}",
        )

    # Tạo order
    order_req = OrderCreate(
        user_id=user_id,
        status=OrderStatusEnum.IDLE.value,
        note=req.note,
    )
    try:
        order = order_repo.create_order(db=db, req=order_req, user_id=user_id)

        order_item_req = OrderItemCreate(
            order_id=order.id,
            prod_id=req.item.prod_id,
            price_per_unit=valid_prod.price,
            count=req.item.count,
        )

        created_item = order_repo.create_order_item(
            db=db, item=order_item_req, user_id=user_id
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    order_items: list[OrderItemView] = []
    total_price = 0.0

    item_view = OrderItemView(
        id=created_item.id,
        prod_id=created_item.product_id,
        prod_name=valid_prod.name,
        price_per_unit=created_item.price,
        count=created_item.count,
    )
    order_items.append(item_view)
    total_price += created_item.price * created_item.count

    return OrderView(
        ord_id=order.id,
        user_id=order.user_id,
        status=order.status,
        status_str=OrderStatus[order.status],
        note=order.note,
        total_price=total_price,
        items=order_items,
    )


def get_my_orders(
    db: Session, user_id: int, query: OrderQueryParams
) -> list[OrderView]:
    """
    Lấy tất cả đơn hàng của user hiện tại.
    """
    orders = order_repo.get_orders_by_user(db=db, user_id=user_id, status=query.status)
    if not orders:
        return []

    # Batch load all order items to avoid N+1 queries.
    order_ids = [o.id for o in orders]
    all_items = order_repo.get_items_by_order_ids(db=db, order_ids=order_ids)

    # Lấy thông tin sản phẩm để map tên + giá
    product_ids = {item.product_id for item in all_items}
    products = prod_repo.get_by_ids(db=db, ids=list(product_ids))
    products_map = {p.id: p for p in products}

    # Map order_id -> list OrderItemView
    items_by_order: dict[int, list[OrderItemView]] = {oid: [] for oid in order_ids}
    total_by_order: dict[int, float] = {oid: 0.0 for oid in order_ids}

    for item in all_items:
        prod = products_map.get(item.product_id)
        prod_name = prod.name if prod else ""
        view = OrderItemView(
            id=item.id,
            prod_id=item.product_id,
            prod_name=prod_name,
            price_per_unit=item.price,
            count=item.count,
        )
        items_by_order[item.order_id].append(view)
        total_by_order[item.order_id] += item.price * item.count

    # Build list OrderView
    result: list[OrderView] = []
    for o in orders:
        result.append(
            OrderView(
                ord_id=o.id,
                user_id=o.user_id,
                status=o.status,
                note=o.note,
                status_str=OrderStatus[o.status],
                total_price=total_by_order.get(o.id, 0.0),
                items=items_by_order.get(o.id, []),
            )
        )

    return result


def get_order_detail(db: Session, user_id: int, order_id: int) -> OrderView | None:
    """
    Xem chi tiết 1 đơn hàng của user.
    """
    order = order_repo.get_order_by_id(db=db, order_id=order_id)
    if not order or order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    items = order_repo.get_items_by_order_id(db=db, order_id=order_id)
    product_ids = {item.product_id for item in items}
    products = prod_repo.get_by_ids(db=db, ids=list(product_ids))
    products_map = {p.id: p for p in products}

    item_views: list[OrderItemView] = []
    total_price = 0.0

    for item in items:
        prod = products_map.get(item.product_id)
        prod_name = prod.name if prod else ""
        view = OrderItemView(
            id=item.id,
            prod_id=item.product_id,
            prod_name=prod_name,
            price_per_unit=item.price,
            count=item.count,
        )
        item_views.append(view)
        total_price += item.price * item.count

    return OrderView(
        ord_id=order.id,
        user_id=order.user_id,
        status=order.status,
        note=order.note,
        status_str=OrderStatus[order.status],
        total_price=total_price,
        items=item_views,
    )


def update_order_status(
    db: Session, user_id: int, order_id: int, new_status: OrderStatusEnum
) -> None:
    """
    Cập nhật trạng thái đơn hàng (simple rule: chỉ chủ sở hữu order được update).
    """
    order = order_repo.get_order_by_id(db=db, order_id=order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    elif order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission",
        )

    current_status = OrderStatusEnum(order.status)

    # update cùng trạng thái thì không làm gì
    if new_status == current_status:
        return

    terminal_statuses = {
        OrderStatusEnum.DONE,
        OrderStatusEnum.CANCEL,
    }

    if current_status in terminal_statuses:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order is already in a terminal state",
        )

    # Cac trang thai duoc phep chuyen tiep
    allowed_transitions = TRANSITIONS.get(current_status, set())
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid status transition: {current_status} -> {new_status}",
        )

    try:
        # thuc hien cac action khi cap nhat sang trang thai moi
        handler = HANDLERS.get(new_status)
        if handler:
            handler.handle(db=db, order=order)

        order_repo.update_order_status(
            db=db, order=order, status=new_status.value, user_id=user_id
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
