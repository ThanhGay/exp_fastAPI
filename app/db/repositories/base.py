from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type
from sqlalchemy import select

ModelType = TypeVar("ModelType")


def apply_limit_offset(query, limit: int | None = None, offset: int | None = None):
    """Áp dụng limit/offset lên query. Dùng chung cho các repository get_multi."""
    if offset is not None and offset > 0:
        query = query.offset(offset)
    if limit is not None and limit > 0:
        query = query.limit(limit)
    return query


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        stmt = select(self.model).where(self.model.id == id)
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(
        self,
        db: Session,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ):
        stmt = select(self.model)
        if offset is not None and offset > 0:
            stmt = stmt.offset(offset)
        if limit is not None and limit > 0:
            stmt = stmt.limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, obj_in):
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.flush()
        return obj