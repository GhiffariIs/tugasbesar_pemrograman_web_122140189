# aturmation_app/models/item.py
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime, # Pastikan DateTime diimpor
    String,
)
from sqlalchemy.sql import func
from .meta import Base
import datetime # Impor modul datetime

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def as_dict(self):
       data = {}
       for c in self.__table__.columns:
           value = getattr(self, c.name)
           if isinstance(value, datetime.datetime): # Periksa jika tipenya datetime
               data[c.name] = value.isoformat()  # Konversi ke string ISO 8601
           else:
               data[c.name] = value
       return data