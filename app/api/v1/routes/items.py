from fastapi import APIRouter, Query
from typing import Annotated
from app.schemas.test.item import CreateItemModel

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.post("/")
async def create_item(item: CreateItemModel):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price * item.tax
    
        item_dict.update({"price_with_tax": price_with_tax, "name": item.name.capitalize()});
    return item_dict

@router.put("/{item_id}")
async def update_item(item_id: int, item: CreateItemModel, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    
    return result

@router.get("/")
async def read_items(q: Annotated[str | None , Query(min_length=3)] ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
