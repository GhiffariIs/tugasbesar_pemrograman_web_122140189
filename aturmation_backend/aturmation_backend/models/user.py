from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode, # Untuk string yang mendukung unicode
    String,  # Bisa juga digunakan untuk string
    DateTime
)
from .meta import Base # Impor Base dari meta.py jika Anda memisahkannya
                       # atau dari . import Base jika Base ada di models/__init__.py
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False) # Simpan hash kata sandi, bukan kata sandi mentah
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Anda mungkin ingin menambahkan relasi atau metode lain di sini