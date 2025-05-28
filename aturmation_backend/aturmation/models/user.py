import bcrypt
import datetime
from sqlalchemy import Column, Integer, Text, Unicode, DateTime, func
from sqlalchemy.orm import validates
import re

from .meta import Base

class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(30), unique=True, nullable=False)
    email = Column(Unicode(100), unique=True, nullable=False)
    name = Column(Unicode(100), nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Unicode(20), default='staff')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    @validates('email')
    def validate_email(self, key, email):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email)
        return email
    
    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 3
        return username
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def set_password(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def by_username(cls, username, db_session):
        return db_session.query(cls).filter_by(username=username).first()
    
    @classmethod
    def by_email(cls, email, db_session):
        return db_session.query(cls).filter_by(email=email).first()
