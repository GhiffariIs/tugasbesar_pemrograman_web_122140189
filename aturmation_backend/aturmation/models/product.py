from sqlalchemy import Column, Integer, Text, Unicode, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import relationship
import datetime

from .meta import Base

class Product(Base):
    """Product model."""
    
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    sku = Column(Unicode(30), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=5)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    category = relationship('Category', back_populates='products')
    creator = relationship('User', foreign_keys=[created_by])
    transactions = relationship('TransactionItem', back_populates='product', cascade='all, delete-orphan')
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.minimum_stock
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'minimum_stock': self.minimum_stock,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'is_low_stock': self.is_low_stock
        }
