from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int | None = Field(None)

    @field_validator('name', 'description', mode='before')
    @classmethod
    def trim_str(cls, v):
        return v.strip() if isinstance(v, str) else v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    id: int


class ProductDelete(BaseModel):
    id: int


class ProductView(ProductBase):
    id: int
    category_name: str | None = None
    model_config = {"from_attributes": True}
