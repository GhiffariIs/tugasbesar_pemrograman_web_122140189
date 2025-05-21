from sqlalchemy import Column, Integer, String
from .meta import Base


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    nama_kategori = Column(String(100), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_kategori': self.nama_kategori,
        }