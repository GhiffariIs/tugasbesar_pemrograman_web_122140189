import unittest
import transaction
import json
from webtest import TestApp
from pyramid.paster import get_app
import os

from ..models.user import User
from ..models.category import Category
from ..models.product import Product
from ..models.transaction import Transaction, TransactionType
from ..models.meta import Base
from ..models import get_engine, get_session_factory, get_tm_session


class FunctionalAPITest(unittest.TestCase):
    """Base class for functional tests of API endpoints."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Get the test.ini file path
        here = os.path.dirname(os.path.abspath(__file__))
        test_ini = os.path.join(here, '..', '..', 'test.ini')
        
        # Create the WSGI app
        cls.app = get_app(test_ini)
        cls.testapp = TestApp(cls.app)
        
        # Get database connection
        settings = cls.app.registry.settings
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)
        
        # Create tables
        Base.metadata.create_all(engine)
        
        cls.session = get_tm_session(session_factory, transaction.manager)
    
    @classmethod
    def tearDownClass(cls):
        """Tear down test environment."""
        # Drop tables
        settings = cls.app.registry.settings
        engine = get_engine(settings)
        Base.metadata.drop_all(engine)
    
    def setUp(self):
        """Set up test data."""
        self.session.query(Transaction).delete()
        self.session.query(Product).delete()
        self.session.query(Category).delete()
        self.session.query(User).delete()
        
        # Create test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        self.session.add(self.user)
        
        # Create test admin
        self.admin = User(username='admin', email='admin@example.com', is_admin=True)
        self.admin.set_password('password')
        self.session.add(self.admin)
        
        # Create test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        
        # Commit the session to get IDs
        self.session.flush()
        
        # Create test product
        self.product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(self.product)
        
        # Commit the session to get IDs
        transaction.commit()
        
        # Store auth token for API calls
        self._login()
    
    def _login(self):
        """Login and get auth token."""
        res = self.testapp.post_json(
            '/api/login',
            {'username': 'testuser', 'password': 'password'},
            status=200
        )
        self.token = res.json['token']
        self.auth_headers = {'Authorization': f'Bearer {self.token}'}
    
    def test_login_endpoint(self):
        """Test login endpoint."""
        # Already tested in _login
        res = self.testapp.post_json(
            '/api/login',
            {'username': 'testuser', 'password': 'password'},
            status=200
        )
        self.assertIn('token', res.json)
        self.assertIn('user', res.json)
    
    def test_user_info_endpoint(self):
        """Test user info endpoint."""
        res = self.testapp.get(
            '/api/user',
            headers=self.auth_headers,
            status=200
        )
        self.assertEqual(res.json['username'], 'testuser')
    
    def test_categories_endpoint(self):
        """Test categories endpoints."""
        # Get all categories
        res = self.testapp.get('/api/categories', status=200)
        self.assertEqual(len(res.json), 1)
        self.assertEqual(res.json[0]['nama_kategori'], 'Test Category')
        
        # Create new category
        res = self.testapp.post_json(
            '/api/categories',
            {'nama_kategori': 'New Category'},
            headers=self.auth_headers,
            status=201
        )
        self.assertEqual(res.json['nama_kategori'], 'New Category')
        
        # Get category by ID
        category_id = res.json['id']
        res = self.testapp.get(f'/api/categories/{category_id}', status=200)
        self.assertEqual(res.json['nama_kategori'], 'New Category')
        
        # Update category
        res = self.testapp.put_json(
            f'/api/categories/{category_id}',
            {'nama_kategori': 'Updated Category'},
            headers=self.auth_headers,
            status=200
        )
        self.assertEqual(res.json['nama_kategori'], 'Updated Category')
        
        # Delete category
        res = self.testapp.delete(
            f'/api/categories/{category_id}',
            headers=self.auth_headers,
            status=200
        )
        self.assertIn('message', res.json)
    
    def test_products_endpoint(self):
        """Test products endpoints."""
        # Get all products
        res = self.testapp.get('/api/products', status=200)
        self.assertEqual(len(res.json), 1)
        self.assertEqual(res.json[0]['nama_produk'], 'Test Product')
        
        # Create new product
        res = self.testapp.post_json(
            '/api/products',
            {
                'nama_produk': 'New Product',
                'kategori_id': self.category.id,
                'stok': 20,
                'harga': 20000,
                'deskripsi': 'New Product Description'
            },
            headers=self.auth_headers,
            status=201
        )
        self.assertEqual(res.json['nama_produk'], 'New Product')
        
        # Get product by ID
        product_id = res.json['id']
        res = self.testapp.get(f'/api/products/{product_id}', status=200)
        self.assertEqual(res.json['nama_produk'], 'New Product')
        
        # Update product
        res = self.testapp.put_json(
            f'/api/products/{product_id}',
            {'nama_produk': 'Updated Product', 'stok': 25},
            headers=self.auth_headers,
            status=200
        )
        self.assertEqual(res.json['nama_produk'], 'Updated Product')
        self.assertEqual(res.json['stok'], 25)
        
        # Delete product
        res = self.testapp.delete(
            f'/api/products/{product_id}',
            headers=self.auth_headers,
            status=200
        )
        self.assertIn('message', res.json)
    
    def test_transactions_endpoint(self):
        """Test transactions endpoints."""
        # Get all transactions (initially empty)
        res = self.testapp.get(
            '/api/transactions',
            headers=self.auth_headers,
            status=200
        )
        self.assertEqual(len(res.json), 0)
        
        # Create new incoming transaction
        res = self.testapp.post_json(
            '/api/transactions',
            {
                'produk_id': self.product.id,
                'jumlah': 5,
                'jenis_transaksi': 'masuk'
            },
            headers=self.auth_headers,
            status=201
        )
        self.assertEqual(res.json['jumlah'], 5)
        self.assertEqual(res.json['jenis_transaksi'], 'masuk')
        self.assertEqual(res.json['current_stock'], 15)  # initial 10 + 5 added
        
        # Create new outgoing transaction
        res = self.testapp.post_json(
            '/api/transactions',
            {
                'produk_id': self.product.id,
                'jumlah': 3,
                'jenis_transaksi': 'keluar'
            },
            headers=self.auth_headers,
            status=201
        )
        self.assertEqual(res.json['jumlah'], 3)
        self.assertEqual(res.json['jenis_transaksi'], 'keluar')
        self.assertEqual(res.json['current_stock'], 12)  # 15 - 3 removed
