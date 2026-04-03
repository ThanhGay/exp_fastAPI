# File cau hinh cac BaseSchema
from sqlalchemy import MetaData, Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from app.db.models.db_schema import DbSchema


class Base(DeclarativeBase):
    pass


class TablenameMixin:
    __schema_prefix__ = None

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__schema_prefix__}_{cls.__name__}"

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


class BaseAuth(TablenameMixin, Base):
    __abstract__ = True
    __schema_prefix__ = DbSchema.AUTH.value
    pass


class BaseProd(TablenameMixin, Base):
    __abstract__ = True
    __schema_prefix__ = DbSchema.PRODUCT.value
    pass


class BaseOrd(TablenameMixin, Base):
    __abstract__ = True
    __schema_prefix__ = DbSchema.ORDER.value
    pass
