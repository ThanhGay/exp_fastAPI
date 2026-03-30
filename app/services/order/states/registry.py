from app.schemas.ord.order import OrderStatusEnum
from app.services.order.states.handlers import (
    ProcessingHandler,
    DeliveringHandler,
    DeliveredHandler,
    DoneHandler,
    RefundHandler,
)

HANDLERS = {
    OrderStatusEnum.PROCESSING: ProcessingHandler(),
    OrderStatusEnum.DELIVERING: DeliveringHandler(),
    OrderStatusEnum.DELIVERED: DeliveredHandler(),
    OrderStatusEnum.DONE: DoneHandler(),
    OrderStatusEnum.CANCEL: RefundHandler(),
}
