from app.models.base import BaseProd
from sqlalchemy import Column, Integer, String, Float, Text

class Product(BaseProd):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)