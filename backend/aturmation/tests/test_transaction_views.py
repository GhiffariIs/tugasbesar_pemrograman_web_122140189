import unittest
from pyramid import testing
import json
from ..models.transaction import Transaction, TransactionType
from ..models.product import Product
from ..models.category import Category
from .base import BaseTest


class TransactionViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
        
        # Add test product
        self.product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(self.product)
        self.session.flush()
        
        # Add test transactions
        self.transaction1 = Transaction(
            produk_id=self.product.id,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        self.transaction2 = Transaction(
            produk_id=self.product.id,
            jumlah=2,
            jenis_transaksi=TransactionType.keluar
        )
        self.session.add(self.transaction1)
        self.session.add(self.transaction2)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_all_transactions(self):
        from ..views.transaction import TransactionView
        
        request = testing.DummyRequest(dbsession=self.session)
        view = TransactionView(request)
        response = view.get_all_transactions()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(len(body), 2)
        
        # Check transactions types
        transaction_types = [trans['jenis_transaksi'] for trans in body]
        self.assertIn('masuk', transaction_types)
        self.assertIn('keluar', transaction_types)
    
    def test_create_transaction_incoming(self):
        from ..views.transaction import TransactionView
        
        initial_stock = self.product.stok
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'produk_id': self.product.id,
                'jumlah': 5,
                'jenis_transaksi': 'masuk'
            }
        )
        view = TransactionView(request)
        response = view.create_transaction()
        
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.body)
        self.assertEqual(body['produk_id'], self.product.id)
        self.assertEqual(body['jumlah'], 5)
        self.assertEqual(body['jenis_transaksi'], 'masuk')
        
        # Check that stock was increased
        self.product = self.session.query(Product).get(self.product.id)
        self.assertEqual(self.product.stok, initial_stock + 5)
    
    def test_create_transaction_outgoing(self):
        from ..views.transaction import TransactionView
        
        initial_stock = self.product.stok
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'produk_id': self.product.id,
                'jumlah': 2,
                'jenis_transaksi': 'keluar'
            }
        )
        view = TransactionView(request)
        response = view.create_transaction()
        
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.body)
        self.assertEqual(body['produk_id'], self.product.id)
        self.assertEqual(body['jumlah'], 2)
        self.assertEqual(body['jenis_transaksi'], 'keluar')
        
        # Check that stock was decreased
        self.product = self.session.query(Product).get(self.product.id)
        self.assertEqual(self.product.stok, initial_stock - 2)
    
    def test_create_transaction_invalid_product(self):
        from ..views.transaction import TransactionView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'produk_id': 9999,  # Nonexistent product
                'jumlah': 5,
                'jenis_transaksi': 'masuk'
            }
        )
        view = TransactionView(request)
        response = view.create_transaction()
        
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertIn('error', body)
        self.assertIn('Product not found', body['error'])
    
    def test_create_transaction_insufficient_stock(self):
        from ..views.transaction import TransactionView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'produk_id': self.product.id,
                'jumlah': 100,  # More than available stock
                'jenis_transaksi': 'keluar'
            }
        )
        view = TransactionView(request)
        response = view.create_transaction()
        
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertIn('error', body)
        self.assertIn('Not enough stock', body['error'])


class TransactionItemViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
        
        # Add test product
        self.product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(self.product)
        self.session.flush()
        
        # Add test transaction
        self.transaction = Transaction(
            produk_id=self.product.id,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        self.session.add(self.transaction)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_transaction(self):
        from ..views.transaction import TransactionItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.transaction.id}
        )
        view = TransactionItemView(request)
        response = view.get_transaction()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(body['produk_id'], self.product.id)
        self.assertEqual(body['jumlah'], 5)
        self.assertEqual(body['jenis_transaksi'], 'masuk')
    
    def test_get_nonexistent_transaction(self):
        from ..views.transaction import TransactionItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': 9999}  # Nonexistent ID
        )
        view = TransactionItemView(request)
        response = view.get_transaction()
        
        self.assertEqual(response.status_code, 404)
        body = json.loads(response.body)
        self.assertIn('error', body)
