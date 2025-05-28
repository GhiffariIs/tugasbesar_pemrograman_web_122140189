from sqlalchemy import Column, Integer, Text, Unicode, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from .meta import Base

class TransactionType(enum.Enum):
    STOCK_IN = 'stock_in'
    STOCK_OUT = 'stock_out'

class Transaction(Base):
    """Transaction model."""
    
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    reference_number = Column(Unicode(50), unique=True, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    creator = relationship('User', foreign_keys=[created_by])
    items = relationship('TransactionItem', back_populates='transaction', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference_number': self.reference_number,
            'transaction_type': self.transaction_type.value,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'creator_name': self.creator.name if self.creator else None,
            'item_count': len(self.items) if self.items else 0,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }

class TransactionItem(Base):
    """Transaction Item model."""
    
    __tablename__ = 'transaction_items'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    transaction = relationship('Transaction', back_populates='items')
    product = relationship('Product', back_populates='transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.quantity * self.unit_price,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
