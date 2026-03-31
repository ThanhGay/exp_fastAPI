from app.schemas.ord.order import OrderStatusEnum
from app.services.order.states.handlers import (
    ProcessingHandler,
    DeliveringHandler,
    DeliveredHandler,
    ReturnRequestedHandler,
    DoneHandler,
    RefundHandler,
)

HANDLERS = {
    OrderStatusEnum.PROCESSING: ProcessingHandler(),
    OrderStatusEnum.DELIVERING: DeliveringHandler(),
    OrderStatusEnum.DELIVERED: DeliveredHandler(),
    OrderStatusEnum.RETURN_REQUESTED: ReturnRequestedHandler(),
    OrderStatusEnum.DONE: DoneHandler(),
    OrderStatusEnum.CANCEL: RefundHandler(),
}
