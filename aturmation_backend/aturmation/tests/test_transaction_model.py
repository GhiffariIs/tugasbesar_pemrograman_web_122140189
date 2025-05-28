import unittest
import transaction as db_transaction
from pyramid import testing
from ..models.transaction import Transaction, TransactionType
from ..models.product import Product
from ..models.category import Category
from .base import BaseTest


class TransactionModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        
        # Add a test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
        
        # Add a test product
        self.product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(self.product)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_transaction_creation(self):
        transaction = Transaction(
            produk_id=self.product.id,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        self.session.add(transaction)
        self.session.flush()
        
        self.assertEqual(transaction.produk_id, self.product.id)
        self.assertEqual(transaction.jumlah, 5)
        self.assertEqual(transaction.jenis_transaksi, TransactionType.masuk)
        self.assertIsNotNone(transaction.tanggal_transaksi)
        
    def test_transaction_enum_values(self):
        self.assertEqual(TransactionType.masuk.value, 'masuk')
        self.assertEqual(TransactionType.keluar.value, 'keluar')
        
    def test_to_dict(self):
        transaction = Transaction(
            produk_id=self.product.id,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        self.session.add(transaction)
        self.session.flush()
        
        trans_dict = transaction.to_dict()
        self.assertEqual(trans_dict['produk_id'], self.product.id)
        self.assertEqual(trans_dict['jumlah'], 5)
        self.assertEqual(trans_dict['jenis_transaksi'], 'masuk')
        self.assertIsNotNone(trans_dict['tanggal_transaksi'])
        self.assertEqual(trans_dict['produk_nama'], 'Test Product')
