from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass

class ProductView(ProductCreate):
    id: int
    model_config = {
        "from_attributes": True
    }