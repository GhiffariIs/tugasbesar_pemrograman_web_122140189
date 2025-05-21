from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    nama_produk = Column(String(100), nullable=False)
    kategori_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    stok = Column(Integer, default=0)
    harga = Column(Float, nullable=False)
    deskripsi = Column(Text, nullable=True)
    
    # Define the relationship to Category
    kategori = relationship("Category", backref="products")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_produk': self.nama_produk,
            'kategori_id': self.kategori_id,
            'stok': self.stok,
            'harga': self.harga,
            'deskripsi': self.deskripsi,
            'kategori_nama': self.kategori.nama_kategori if self.kategori else None
        }