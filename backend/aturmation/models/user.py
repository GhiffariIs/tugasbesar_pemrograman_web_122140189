from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean
from sqlalchemy.sql import func
from .meta import Base
from passlib.hash import bcrypt


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_admin = Column(Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)
        
    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_admin': self.is_admin
        }