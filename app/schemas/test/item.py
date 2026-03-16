from pydantic import BaseModel

class CreateItemModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ViewItemModel(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    