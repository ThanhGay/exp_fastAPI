from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.repositories.catalog import category_repository as repo
from app.schemas.catalog.category import CategoryCreate, CategoryUpdate, CategoryDelete
from app.schemas.common import BaseQueryParams


def create_category(db: Session, req: CategoryCreate, user_id: int):
    print(f"Data create category: {req}")

    if repo.exist_name(db=db, name=req.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name is already exist"
        )

    if req.parent_id:
        if not repo.exist_id(db=db, id=req.parent_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parent_id"
            )

    return repo.create(db=db, req=req, user_id=user_id)


def get_all_categories(db: Session, query: BaseQueryParams | None = None):
    params = query or BaseQueryParams()
    return repo.get_categories(
        db,
        limit=params.limit,
        offset=params.offset,
        keyword=params.keyword,
    )


def get_by_id_category(db: Session, id: int):
    return repo.get_category_by_id(db, id)


def update_category(db: Session, req: CategoryUpdate, user_id: int):
    print(f"Data update category: {req}")
    if not repo.exist_id(db=db, id=req.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if repo.exist_name_exclude_id(db=db, id=req.id, name=req.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name is already exist"
        )

    if req.parent_id:
        if not repo.exist_id(db=db, id=req.parent_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid parent_id"
            )

    return repo.update_category(db=db, req=req, user_id=user_id)


def soft_delete_category(db: Session, req: CategoryDelete, user_id: int) -> bool:
    print(f"CategoryId delete: {req.id}")

    category = repo.get_category_by_id(db=db, id=req.id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return repo.delete(db, req.id, user_id)
