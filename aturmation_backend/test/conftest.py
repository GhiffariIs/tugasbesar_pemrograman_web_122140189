# tests/conftest.py
import pytest
from webtest import TestApp
from sqlalchemy import create_engine # Kita mungkin tidak perlu ini jika mengambil engine dari app
from sqlalchemy.orm import sessionmaker
from pyramid.request import Request

from aturmation_app.models.meta import Base
from aturmation_app.models import (
    User, UserRole, Category, Product, Transaction, TransactionType
    # DBSession global tidak perlu diimpor/dikonfigurasi dari sini jika app mengelola via factory
)

from aturmation_app import main as main_app_factory

@pytest.fixture(scope='session')
def test_settings_override():
    """Override settings aplikasi khusus untuk lingkungan tes."""
    return {
        'sqlalchemy.url': 'sqlite:///:memory:',
        'jwt.secret': 'test-jwt-secret-for-pytest',
        # Pastikan pyramid_tm di-include oleh main_app_factory Anda
    }

@pytest.fixture(scope='session')
def pyramid_app_with_db_schema(test_settings_override):
    """
    Membuat instance aplikasi DAN memastikan database (tabel) dibuat
    pada engine yang digunakan oleh aplikasi tersebut.
    """
    # 1. Buat instance aplikasi. Ini akan menjalankan main_app_factory,
    #    yang akan memanggil config.include('.models'), yang kemudian
    #    menjalankan 'includeme' di models/__init__.py.
    #    'includeme' akan membuat engine berdasarkan 'sqlalchemy.url' dari test_settings_override
    #    dan menyimpan session_factory yang terikat ke engine tersebut di registry.
    app = main_app_factory({}, **test_settings_override)

    # 2. Dapatkan engine yang dibuat dan digunakan oleh aplikasi dari registry.
    #    Di models/__init__.py Anda, Anda menyimpan session_factory.
    #    Engine terikat pada session_factory tersebut.
    dbsession_factory_from_app = app.registry['dbsession_factory']
    engine_used_by_app = dbsession_factory_from_app.kw['bind'] # Engine ada di factory.kw['bind']
    
    assert engine_used_by_app is not None, "Engine tidak ditemukan dari dbsession_factory aplikasi"
    assert str(engine_used_by_app.url) == test_settings_override['sqlalchemy.url'], \
        "Engine aplikasi tidak cocok dengan URL tes (SQLite in-memory)"

    # 3. Buat semua tabel pada engine yang digunakan oleh aplikasi.
    Base.metadata.create_all(engine_used_by_app)
    
    yield app # Sediakan aplikasi yang sudah siap dengan DB

    # 4. Bersihkan setelah semua tes dalam sesi selesai
    Base.metadata.drop_all(engine_used_by_app)
    engine_used_by_app.dispose()

@pytest.fixture
def testapp(pyramid_app_with_db_schema):
    """Menyediakan instance TestApp untuk melakukan request HTTP."""
    return TestApp(pyramid_app_with_db_schema)

@pytest.fixture(scope='function')
def dbsession(pyramid_app_with_db_schema, request): # pyramid_app_with_db_schema untuk akses engine aplikasi
    """
    Menyediakan sesi DB terisolasi per fungsi tes untuk setup/verifikasi data manual.
    Ini menggunakan engine yang sama dengan yang digunakan aplikasi.
    """
    # Dapatkan engine yang sama yang digunakan oleh aplikasi
    dbsession_factory_from_app = pyramid_app_with_db_schema.registry['dbsession_factory']
    engine = dbsession_factory_from_app.kw['bind']
    
    connection = engine.connect()
    transaction = connection.begin() # Mulai transaksi DB untuk isolasi data tes
    
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    def teardown():
        session.close()
        transaction.rollback() # Rollback semua perubahan yang dibuat di sesi ini
        connection.close()

    request.addfinalizer(teardown)
    return session

@pytest.fixture
def dummy_request(dbsession, pyramid_app_with_db_schema):
    """Membuat objek request Pyramid dummy."""
    req = Request.blank('/')
    req.dbsession = dbsession 
    req.registry = pyramid_app_with_db_schema.registry
    return req

# --- Fixture Factories untuk Membuat Data Tes ---
# Pastikan mereka menggunakan 'dbsession' yang di-inject dan memanggil dbsession.commit()
# agar data terlihat oleh request 'testapp' yang berjalan dalam transaksi terpisah.

@pytest.fixture
def create_test_user(dbsession):
    def _create_test_user(name, username, email, password, role=UserRole.staff, commit_session=True):
        user = User(name=name, username=username, email=email, role=role)
        user.set_password(password)
        dbsession.add(user)
        if commit_session:
            dbsession.commit() # Commit agar terlihat oleh request testapp
        else:
            dbsession.flush()
        return user
    return _create_test_user

@pytest.fixture
def create_test_category(dbsession):
    def _create_test_category(name, description=None, commit_session=True):
        category = Category(name=name, description=description)
        dbsession.add(category)
        if commit_session:
            dbsession.commit()
        else:
            dbsession.flush()
        return category
    return _create_test_category

@pytest.fixture
def create_test_product(dbsession, create_test_category):
    def _create_test_product(name, sku, price, stock, min_stock, category_id=None, category_name=None, commit_session=True):
        if category_id is None:
            target_category_name = category_name if category_name else "Default Test Category Product"
            cat = dbsession.query(Category).filter_by(name=target_category_name).first()
            if not cat:
                cat = create_test_category(name=target_category_name, commit_session=True)
            category_id = cat.id
        
        product = Product(
            name=name, sku=sku, description=f"Desc for {name}", price=price, stock=stock,
            min_stock=min_stock, category_id=category_id
        )
        dbsession.add(product)
        if commit_session:
            dbsession.commit()
        else:
            dbsession.flush()
        return product
    return _create_test_product

@pytest.fixture
def auth_token_for_user(testapp, create_test_user):
    def _auth_token_for_user(username, password, name=None, email=None, role=UserRole.staff):
        user_name = name if name else f"Test User {username}"
        user_email = email if email else f"{username}_{role.value}_token_auto@example.com"
        
        # create_test_user dipanggil dengan commit_session=True
        create_test_user(
            name=user_name, username=username, email=user_email,
            password=password, role=role, commit_session=True
        )
        
        login_payload = {'username': username, 'password': password}
        res = testapp.post_json('/api/v1/auth/login', login_payload, expect_errors=True)
        
        if res.status_code == 200:
            token = res.json.get('token')
            if token: return token
            print(f"Login OK (200) but no token for {username}. Response: {res.json}")
            return None
        else:
            response_text = res.json if res.content_type == 'application/json' else res.text
            print(f"Login failed in auth_token_for_user for {username}. Status: {res.status_code}, Response: {response_text}")
            return None
    return _auth_token_for_user