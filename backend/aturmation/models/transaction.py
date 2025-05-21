from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base
import enum


class TransactionType(enum.Enum):
    masuk = "masuk"
    keluar = "keluar"


class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    produk_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    jumlah = Column(Integer, nullable=False)
    jenis_transaksi = Column(Enum(TransactionType), nullable=False)
    tanggal_transaksi = Column(DateTime, default=func.now())
    
    # Define the relationship to Product
    produk = relationship("Product", backref="transactions")
    
    def to_dict(self):
        return {
            'id': self.id,
            'produk_id': self.produk_id,
            'jumlah': self.jumlah,
            'jenis_transaksi': self.jenis_transaksi.value,
            'tanggal_transaksi': self.tanggal_transaksi.isoformat() if self.tanggal_transaksi else None,
            'produk_nama': self.produk.nama_produk if self.produk else None
        }