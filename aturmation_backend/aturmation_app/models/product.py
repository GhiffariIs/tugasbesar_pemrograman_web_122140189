# aturmation_app/models/product.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float
)
from sqlalchemy.sql import func
from .meta import Base
import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0) # Stok tetap ada

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime.datetime) else None,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime.datetime) else None
        }