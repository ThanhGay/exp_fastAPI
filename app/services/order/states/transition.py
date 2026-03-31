from app.schemas.ord.order import OrderStatusEnum

TRANSITIONS = {
    OrderStatusEnum.IDLE: {OrderStatusEnum.PROCESSING, OrderStatusEnum.CANCEL},
    OrderStatusEnum.PROCESSING: {OrderStatusEnum.DELIVERING, OrderStatusEnum.CANCEL},
    OrderStatusEnum.DELIVERING: {OrderStatusEnum.DELIVERED},
    OrderStatusEnum.DELIVERED: {
        OrderStatusEnum.DONE,
        OrderStatusEnum.CANCEL,
        OrderStatusEnum.RETURN_REQUESTED,
    },
    OrderStatusEnum.RETURN_REQUESTED: {OrderStatusEnum.DELIVERED},
}
