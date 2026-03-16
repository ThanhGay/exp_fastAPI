# File cau hinh cac BaseSchema
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from app.models.db_schema import DbSchema

from typing import Any
from sqlalchemy.ext.declarative import declared_attr

class TablenameMixin:
    """Chung logic __tablename__ giống Base."""
    id: Any
    __name__: str
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.capitalize()

# Cụm auth (User, Role, Permission...)
metadata_auth = MetaData(schema=DbSchema.AUTH.value)

class BaseAuth (TablenameMixin, DeclarativeBase):
    # metadata=metadata_auth
    pass




# Cụm prod (Product, Category...)
metadata_prod = MetaData(schema=DbSchema.PRODUCT.value)

class BaseProd (TablenameMixin, DeclarativeBase):
    # metadata=metadata_prod
    pass