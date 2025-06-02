# tests/conftest.py
import pytest
from webtest import TestApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyramid.request import Request

from aturmation_app.models.meta import Base
from aturmation_app.models import (
    User, UserRole, Product, # HANYA User, UserRole, Product
    DBSession # Impor DBSession global dari models
)
from aturmation_app import main as main_app_factory

@pytest.fixture(scope='session')
def test_settings_override():
    return {
        'sqlalchemy.url': 'sqlite:///:memory:',
        'jwt.secret': 'test-jwt-secret-for-pytest',
    }

@pytest.fixture(scope='session')
def test_engine(test_settings_override):
    return create_engine(test_settings_override['sqlalchemy.url'])

@pytest.fixture(scope='session')
def setup_database_schema(test_engine):
    DBSession.configure(bind=test_engine)
    Base.metadata.create_all(test_engine) # Hanya akan membuat tabel User dan Product
    yield
    Base.metadata.drop_all(test_engine)
    if hasattr(DBSession, 'remove'): DBSession.remove()

@pytest.fixture(scope='session')
def pyramid_app(test_settings_override, setup_database_schema): # Bergantung pada setup_database_schema
    # DBSession global sudah dikonfigurasi oleh setup_database_schema
    app = main_app_factory({}, **test_settings_override)
    return app

@pytest.fixture
def testapp(pyramid_app):
    return TestApp(pyramid_app)

@pytest.fixture(scope='function')
def dbsession(test_engine, request): # Sesi lokal untuk setup/verifikasi tes
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()
    request.addfinalizer(teardown)
    return session

@pytest.fixture
def dummy_request(dbsession, pyramid_app):
    req = Request.blank('/')
    req.dbsession = dbsession 
    req.registry = pyramid_app.registry
    return req

@pytest.fixture
def create_test_user(dbsession):
    def _create_test_user(name, username, email, password, role=UserRole.staff, commit_session=True):
        user = User(name=name, username=username, email=email, role=role)
        user.set_password(password)
        dbsession.add(user)
        if commit_session:
            dbsession.commit()
        else:
            dbsession.flush()
        return user
    return _create_test_user

@pytest.fixture
def create_test_product(dbsession): # Tidak perlu create_test_category lagi
    def _create_test_product(name, sku, price, stock, description=None, commit_session=True):
        product = Product(
            name=name, sku=sku, description=description, price=price, stock=stock
            # Tidak ada category_id, min_stock (jika dihapus dari model)
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