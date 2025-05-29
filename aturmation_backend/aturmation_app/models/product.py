from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float, # Untuk harga, bisa juga Numeric atau Decimal tergantung presisi yang dibutuhkan
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base # Asumsi meta.py ada di direktori yang sama (models)
import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False, unique=True) # Stock Keeping Unit
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False) # Asumsi harga bisa desimal
    stock = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0) # Untuk notifikasi stok rendah

    # Foreign Key ke tabel categories
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Relasi ke model Category (untuk akses mudah objek Category dari Product)
    # back_populates memberitahu SQLAlchemy sisi lain dari relasi ini di model Category
    category = relationship("Category", back_populates="products") 

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def as_dict(self, include_category_details=True):
        data = {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "min_stock": self.min_stock,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime.datetime) else None,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime.datetime) else None
        }
        if include_category_details and self.category:
            data['category'] = {
                "id": self.category.id,
                "name": self.category.name
                # Tambahkan field lain dari kategori jika perlu
            }
        elif include_category_details: # Jika category belum di-load atau tidak ada
            data['category'] = None
        return data