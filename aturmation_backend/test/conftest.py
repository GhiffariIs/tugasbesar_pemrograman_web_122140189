import pytest
from webtest import TestApp
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# from transaction import TestingTransactionManager

# Impor Base dan semua model Anda
from aturmation_app.models.meta import Base
from aturmation_app.models import User, UserRole, Category, Product, Transaction, TransactionType 

from aturmation_app import main as main_app_factory

@pytest.fixture(scope='session')
def test_settings_override():
    return {
        'sqlalchemy.url': 'sqlite:///:memory:', 
        'jwt.secret': 'test-jwt-secret-key',
    }

@pytest.fixture(scope='session')
def pyramid_app(test_settings_override):
    app = main_app_factory({}, **test_settings_override)
    return app

@pytest.fixture # Scope 'function' lebih aman untuk testapp jika ada state yang bisa berubah
def testapp(pyramid_app):
    return TestApp(pyramid_app)

@pytest.fixture(scope='function') 
def db_session(pyramid_app, test_settings_override, request):
    engine = create_engine(test_settings_override['sqlalchemy.url'])
    Base.metadata.create_all(engine) 
    Session = scoped_session(sessionmaker(bind=engine))
    dbsession = Session()

    # Hapus bagian yang berkaitan dengan TestingTransactionManager
    # tm = TestingTransactionManager() 
    # request.addfinalizer(tm.abort) 
    # dbsession.transaction_manager = tm 

    # Untuk pyramid_tm, sesi biasanya sudah terikat dengan transaction manager
    # saat request dibuat. Untuk TestApp, ini ditangani oleh pyramid_tm.
    # Jika Anda memanggil view secara langsung dengan dummy_request,
    # Anda mungkin perlu `transaction.begin()` dan `transaction.commit()/abort()`
    # atau gunakan `with transaction.manager:`

    def teardown():
        dbsession.close() # Pastikan sesi ditutup
        Base.metadata.drop_all(engine) 
        engine.dispose()

    request.addfinalizer(teardown)
    return dbsession

# ... (sisa fixtures seperti dummy_request, create_test_user, dll. tetap sama) ...
@pytest.fixture
def dummy_request(db_session, pyramid_app):
    from pyramid.request import Request
    request = Request.blank('/') 
    request.dbsession = db_session
    request.registry = pyramid_app.registry 
    return request

@pytest.fixture
def create_test_user(db_session):
    def _create_test_user(name, username, email, password, role=UserRole.staff, save=True):
        user = User(name=name, username=username, email=email, role=role)
        user.set_password(password)
        if save:
            db_session.add(user)
            db_session.commit() 
        return user
    return _create_test_user

@pytest.fixture
def create_test_category(db_session):
    def _create_test_category(name, description=None, save=True):
        category = Category(name=name, description=description)
        if save:
            db_session.add(category)
            db_session.commit()
        return category
    return _create_test_category

@pytest.fixture
def create_test_product(db_session, create_test_category): # Bisa inject fixture lain
    def _create_test_product(name, sku, price, stock, min_stock, category_id=None, category_name=None, save=True):
        if category_id is None and category_name:
            # Buat kategori jika belum ada atau cari berdasarkan nama
            cat = db_session.query(Category).filter_by(name=category_name).first()
            if not cat:
                cat = create_test_category(name=category_name, save=True)
            category_id = cat.id
        elif category_id is None:
            # Buat kategori default jika tidak ada ID atau nama yang diberikan
            cat = create_test_category(name="Default Test Category", save=True)
            category_id = cat.id

        product = Product(
            name=name, sku=sku, price=price, stock=stock,
            min_stock=min_stock, category_id=category_id
        )
        if save:
            db_session.add(product)
            db_session.commit()
        return product
    return _create_test_product


@pytest.fixture
def auth_token_for_user(testapp, create_test_user, db_session):
    def _auth_token_for_user(username, password, name="Test User For Token", email_prefix="tokenuser", role=UserRole.staff):
        # Cek apakah user ada, jika tidak buat
        user = db_session.query(User).filter_by(username=username).first()
        if not user:
            user = create_test_user(
                name=name,
                username=username,
                email=f"{email_prefix}_{username}@example.com",
                password=password,
                role=role,
                save=True
            )
        # db_session.commit() # Pastikan user tersimpan sebelum login

        login_payload = {'username': username, 'password': password}
        # Perbolehkan 401 jika login memang sengaja diuji untuk gagal
        res = testapp.post_json('/api/v1/auth/login', login_payload, expect_errors=True) 
        if res.status_code == 200:
            return res.json.get('token')
        elif res.status_code == 401:
            print(f"Login failed for user {username} in auth_token_for_user: {res.json}")
            return None
        else: # Error lain
            print(f"Unexpected status {res.status_code} for user {username} in auth_token_for_user: {res.text}")
            res.showbrowser() # Tampilkan detail error dari webtest
            return None 
    return _auth_token_for_user