from sqlalchemy import Column, Integer, Text, Unicode, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from .meta import Base

class Category(Base):
    """Category model."""
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    creator = relationship('User', foreign_keys=[created_by])
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'product_count': len(self.products) if self.products else 0
        }
