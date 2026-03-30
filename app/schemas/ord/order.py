from enum import Enum
from pydantic import BaseModel, Field, field_validator


class OrderStatusEnum(int, Enum):
    IDLE = 0
    PROCESSING = 1
    DELIVERING = 2
    DONE = 3
    CANCEL = 4


OrderStatus = dict(
    {
        OrderStatusEnum.IDLE: "Tao moi",
        OrderStatusEnum.PROCESSING: "Dang xu ly",
        OrderStatusEnum.DELIVERING: "Dang van chuyen",
        OrderStatusEnum.DONE: "Da nhan hang",
        OrderStatusEnum.CANCEL: "Da huy",
    }
)


class OrderItemBase(BaseModel):
    prod_id: int
    price_per_unit: float | None = None
    count: int


class OrderItemCreate(OrderItemBase):
    order_id: int | None = Field(None)

    @field_validator("count")
    def validate_count(cls, v):
        if v <= 0:
            raise ValueError("Count cannot less or equals than 0")
        return v


class OrderItemView(OrderItemBase):
    id: int
    prod_name: str


class OrderBase(BaseModel):
    status: int | None = Field(None)
    note: str | None = Field(None)


class OrderCreate(OrderBase):
    pass


class OrderView(OrderBase):
    user_id: int
    ord_id: int
    total_price: float
    status_str: str | None = None
    items: list[OrderItemView]


class OrderCreateFromCart(BaseModel):
    item_ids: list[int]


class OrderCreateDirect(OrderBase):
    item: OrderItemCreate


class OrderUpdateStatus(BaseModel):
    status: int
