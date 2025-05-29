from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base
import datetime

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="category")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime.datetime) else None,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime.datetime) else None
        }