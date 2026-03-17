from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type
from sqlalchemy import select

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        stmt = select(self.model).where(self.model.id == id)
        return db.execute(stmt).scalar_one_or_none()

    def get_multi(self, db: Session):
        stmt = select(self.model)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, obj_in):
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj