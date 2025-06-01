from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SAEnum # Menggunakan SAEnum dari SQLAlchemy
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .meta import Base
import datetime
import enum # Modul enum Python standar

# Definisikan Enum untuk Tipe Transaksi di Python
class TransactionType(enum.Enum):
    stock_in = "stock_in"         # Barang masuk (pembelian, penerimaan)
    stock_out = "stock_out"       # Barang keluar (penjualan, penggunaan)
    initial_stock = "initial_stock" # Stok awal saat produk pertama kali dibuat/dimigrasi
    adjustment = "adjustment"     # Penyesuaian stok (misalnya, karena stock opname)
    # Tambahkan tipe lain jika perlu

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    # Relasi ke Product (opsional, tapi berguna untuk akses mudah)
    product = relationship("Product") # Tidak perlu back_populates jika Product tidak punya list transactions

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # Siapa yang melakukan transaksi
    # Relasi ke User (opsional)
    user = relationship("User")

    type = Column(SAEnum(TransactionType), nullable=False) # Menggunakan Enum yang sudah didefinisikan
    quantity = Column(Integer, nullable=False) # Jumlah barang yang terlibat
                                              # Harus positif. Validasi di view.
    notes = Column(Text, nullable=True) # Catatan tambahan
    timestamp = Column(DateTime, default=func.now()) # Waktu transaksi

    def as_dict(self, include_product_details=False, include_user_details=False):
        data = {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "type": self.type.value if self.type else None, # Ambil .value dari enum
            "quantity": self.quantity,
            "notes": self.notes,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime.datetime) else None
        }
        if include_product_details and self.product:
            data['product'] = {
                "id": self.product.id,
                "name": self.product.name,
                "sku": self.product.sku
            }
        if include_user_details and self.user:
            data['user'] = {
                "id": self.user.id,
                "username": self.user.username,
                "name": self.user.name
            }
        return data