# aturmation_app/models/user.py
from sqlalchemy import Column, Integer, Text, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

from .meta import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(Text, nullable=False)
    # Tetap simpan kolom role untuk kompatibilitas
    role = Column(String(20), nullable=False, default='user')
    photo = Column(Text, nullable=True)

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)
        
    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'photo': self.photo
            # Tidak perlu menampilkan role ke client
        }
