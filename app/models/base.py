# File cau hinh cac BaseSchema
from sqlalchemy import MetaData, Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from app.models.db_schema import DbSchema

class TablenameMixin:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)
    @declared_attr
    def created_by(cls):
        return Column(Integer, nullable=True)
    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=func.now())
    @declared_attr
    def modified_by(cls):
        return Column(Integer, nullable=True)
    @declared_attr
    def modified_at(cls):
        return Column(DateTime, nullable=True)
    @declared_attr
    def deleted_by(cls):
        return Column(Integer, nullable=True)
    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)
    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, nullable=False, default=False, server_default="0")
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