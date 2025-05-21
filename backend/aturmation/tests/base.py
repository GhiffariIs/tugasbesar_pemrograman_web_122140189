import unittest
import transaction
from pyramid import testing
from webtest import TestApp

from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.meta import Base
from ..models.user import User
from ..models.category import Category
from ..models.product import Product
from ..models.transaction import Transaction, TransactionType


def dummy_request(dbsession):
    """Create a dummy request with a dbsession."""
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    """Base test class for all tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:',
            'jwt.secret': 'testsecret',
            'jwt.algorithm': 'HS256',
            'jwt.expiration': '3600',
        })
        self.config.include('..models')
        self.config.include('..routes')
        
        # Set up request.auth_policy method
        from ..security.jwt import MyAuthenticationPolicy
        authn_policy = MyAuthenticationPolicy(self.config.registry.settings)
        self.config.registry.registerUtility(authn_policy, MyAuthenticationPolicy)
        self.config.add_request_method(
            lambda request: request.registry.getUtility(MyAuthenticationPolicy), 
            'auth_policy', 
            reify=True
        )
        
        # Set up request.user method
        from ..security.jwt import get_user
        self.config.add_request_method(get_user, 'user', reify=True)
        
        # Register User class in registry
        self.config.registry.User = User
        
        # Setup database
        engine = get_engine(self.config.registry.settings)
        session_factory = get_session_factory(engine)
        self.session = get_tm_session(session_factory, transaction.manager)
        
        # Create tables
        Base.metadata.create_all(engine)
    
    def tearDown(self):
        """Clean up test environment."""
        testing.tearDown()
        transaction.abort()
        
    def init_database(self):
        """Initialize test database with sample data."""
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        self.session.add(user)
        
        # Create test admin
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('password')
        self.session.add(admin)
        
        # Create test categories
        category1 = Category(nama_kategori='Test Category 1')
        category2 = Category(nama_kategori='Test Category 2')
        self.session.add(category1)
        self.session.add(category2)
        
        # Create test products
        product1 = Product(
            nama_produk='Test Product 1',
            kategori_id=1,
            stok=10,
            harga=10000,
            deskripsi='Test Description 1'
        )
        product2 = Product(
            nama_produk='Test Product 2',
            kategori_id=2,
            stok=20,
            harga=20000,
            deskripsi='Test Description 2'
        )
        self.session.add(product1)
        self.session.add(product2)
        
        # Create test transactions
        transaction1 = Transaction(
            produk_id=1,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        transaction2 = Transaction(
            produk_id=2,
            jumlah=3,
            jenis_transaksi=TransactionType.keluar
        )
        self.session.add(transaction1)
        self.session.add(transaction2)


class FunctionalTest(unittest.TestCase):
    """Base class for functional tests."""
    
    def setUp(self):
        """Set up test environment."""
        from .. import main
        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:',
            'jwt.secret': 'testsecret',
            'jwt.algorithm': 'HS256',
            'jwt.expiration': '3600',
        }
        app = main({}, **settings)
        self.testapp = TestApp(app)
        
        # Setup database
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)
        self.session = get_tm_session(session_factory, transaction.manager)
        
        # Create tables
        Base.metadata.create_all(engine)
        
        # Initialize database
        self.init_database()
        
    def tearDown(self):
        """Clean up test environment."""
        transaction.abort()
        
    def init_database(self):
        """Initialize test database with sample data."""
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        self.session.add(user)
        
        # Create test admin
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('password')
        self.session.add(admin)
        
        # Create test categories
        category1 = Category(nama_kategori='Test Category 1')
        category2 = Category(nama_kategori='Test Category 2')
        self.session.add(category1)
        self.session.add(category2)
        
        # Create test products
        product1 = Product(
            nama_produk='Test Product 1',
            kategori_id=1,
            stok=10,
            harga=10000,
            deskripsi='Test Description 1'
        )
        product2 = Product(
            nama_produk='Test Product 2',
            kategori_id=2,
            stok=20,
            harga=20000,
            deskripsi='Test Description 2'
        )
        self.session.add(product1)
        self.session.add(product2)
        
        # Create test transactions
        transaction1 = Transaction(
            produk_id=1,
            jumlah=5,
            jenis_transaksi=TransactionType.masuk
        )
        transaction2 = Transaction(
            produk_id=2,
            jumlah=3,
            jenis_transaksi=TransactionType.keluar
        )
        self.session.add(transaction1)
        self.session.add(transaction2)
        
        # Commit the changes
        transaction.commit()
