from pydantic import BaseModel, Field, field_validator


class BaseCartItem(BaseModel):
    product_id: int = Field(...)
    count: int = Field(..., min=1)


class CartItemView(BaseCartItem):
    id: int
    product_name: str | None = Field(None)
    price_per_unit: float | None = Field(None)


class CartItemCreate(BaseCartItem):

    @field_validator("count")
    def validate_count(cls, v):
        if v <= 0:
            raise ValueError("Count cannot less or equals than 0")
        return v


class CartItemDelete(BaseModel):
    id: int
