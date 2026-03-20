from pydantic import BaseModel, field_validator

class CategoryView(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    description: str | None = None
    parent_id: int | None = None

    @field_validator('name', 'description', mode='before')
    @classmethod
    def trim_str(cls, v):
        return v.strip() if isinstance(v, str) else v

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    parent_id: int | None = None

class CategoryUpdate(CategoryCreate):
    id: int

class CategoryDelete(BaseModel):
    id: int
