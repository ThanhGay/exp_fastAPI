from pydantic import BaseModel

class CategoryView(BaseModel):
    id: int
    name: str
    description: str | None = None
    parent_id: int | None = None

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    parent_id: int | None = None

class CategoryUpdate(CategoryCreate):
    id: int

class CategoryDelete(BaseModel):
    id: int
