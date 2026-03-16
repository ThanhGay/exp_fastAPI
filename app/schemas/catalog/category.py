from pydantic import BaseModel

class CategoryModel(BaseModel):
    id: int
    name: str
    description: str | None = None

class SubCategoryModel(CategoryModel):
    parent_id: int

class CreateCategoryModel(BaseModel):
    name: str
    description: str | None = None