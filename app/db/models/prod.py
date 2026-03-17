from app.db.models.base import BaseProd
from sqlalchemy import Column, Integer, String, Float, Text

class Product(BaseProd):
    __tablename__ = "Product"
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, nullable=True)

class Category(BaseProd):
    name = Column(String(255), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, index=True)