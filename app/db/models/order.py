from app.db.models.base import BaseOrd
from sqlalchemy import Column, Integer, String, Text, Float


class Cart(BaseOrd):
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    count = Column(Integer)


class Order(BaseOrd):
    user_id = Column(Integer, nullable=False)
    status = Column(Integer, default=0)
    note = Column(Text)


class OrderItem(BaseOrd):
    __tablename__ = "OrderItem"

    order_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    count = Column(Integer)
    price = Column(Float)
