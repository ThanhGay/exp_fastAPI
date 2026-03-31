from app.schemas.catalog.category import CategoryCreate, CategoryUpdate
from app.db.models.prod import Category
from app.db.repositories.base import apply_limit_offset
from sqlalchemy.orm import Session
from sqlalchemy import and_, exists, or_
from datetime import datetime, timezone


# CREATE
def create(db: Session, req: CategoryCreate, user_id: int) -> Category:
    new_category = Category(
        name=req.name,
        description=req.description,
        parent_id=req.parent_id,
        created_by=user_id,
    )

    db.add(new_category)
    db.flush()

    return new_category


# READ - many
def get_categories(
    db: Session,
    *,
    limit: int | None = None,
    offset: int | None = None,
    keyword: str | None = None,
):
    res = db.query(Category).where(Category.is_deleted != True)
    if keyword:
        pattern = f"%{keyword}%"
        res = res.filter(
            or_(
                Category.name.ilike(pattern),
                Category.description.ilike(pattern),
            )
        )
    res = apply_limit_offset(res, limit=limit, offset=offset)
    return res.all()


# READ - one by id
def get_category_by_id(db: Session, id: int) -> Category:
    return (
        db.query(Category)
        .filter(Category.id == id, Category.is_deleted != True)
        .first()
    )


# UPDATE
def update_category(db: Session, req: CategoryUpdate, user_id: int) -> Category:
    category = get_category_by_id(db=db, id=req.id)

    if not category:
        return None

    category.name = req.name
    category.description = req.description
    category.parent_id = req.parent_id

    category.modified_at = datetime.now(tz=timezone.utc)
    category.modified_by = user_id

    db.flush()

    return category


# DELETE - soft delete
def delete(db: Session, id: int, user_id: int) -> bool:
    category = get_category_by_id(db=db, id=id)

    if not category:
        return False

    category.is_deleted = True
    category.deleted_at = datetime.now(tz=timezone.utc)
    category.deleted_by = user_id

    db.flush()

    return True


# DELETE - permanent delete
def remove(db: Session, id: int) -> bool:
    category = get_category_by_id(db=db, id=id)

    if not category:
        return False

    db.delete(category)
    db.flush()

    return True


def exist_id(db: Session, id: int) -> bool:
    return db.query(exists().where(Category.id == id)).scalar()


def exist_name(db: Session, name: str) -> bool:
    return db.query(exists().where(Category.name == name)).scalar()


def exist_name_exclude_id(db: Session, id: int, name: str):
    return db.query(
        exists().where(and_(Category.name == name, Category.id != id))
    ).scalar()
