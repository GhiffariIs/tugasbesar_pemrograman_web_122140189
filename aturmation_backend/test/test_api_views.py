import pytest
import transaction
from pyramid import testing
from webtest import TestApp # Untuk testing aplikasi WSGI

from aturmation_app import main # Impor fungsi main dari __init__.py aplikasi Anda
from aturmation_app.models import DBSession, Item, User # Impor model dan DBSession
from aturmation_app.models.meta import Base

# Fixture untuk konfigurasi aplikasi (dijalankan sekali per sesi tes)
@pytest.fixture(scope='session')
def testapp_settings(tmpdir_factory):
    # Gunakan database SQLite in-memory untuk testing agar cepat dan terisolasi
    # Atau siapkan database test PostgreSQL terpisah
    db_path = str(tmpdir_factory.mktemp("data").join("test.sqlite"))
    return {
        'sqlalchemy.url': f'sqlite:///{db_path}', # Gunakan SQLite untuk tes
        'pyramid.includes': [
            'pyramid_tm',
            'aturmation_app.models',
            'aturmation_app.security',
            'aturmation_app.routes',
        ],
        # 'auth.secret': 'testsecret', # Jika ada konfigurasi auth tambahan
    }

# Fixture untuk aplikasi TestApp (dijalankan sekali per sesi tes)
@pytest.fixture(scope='session')
def testapp(testapp_settings):
    app = main({}, **testapp_settings)
    return TestApp(app)

# Fixture untuk sesi database (dijalankan per fungsi tes)
@pytest.fixture(scope='function')
def db_session(testapp_settings, request):
    engine = sqlalchemy.create_engine(testapp_settings['sqlalchemy.url'])
    Base.metadata.create_all(engine) # Buat skema DB untuk setiap tes
    session_factory = sessionmaker(bind=engine)
    DBSession.configure(bind=engine) # Konfigurasi DBSession global jika digunakan
    session = DBSession()

    # Tambahkan user untuk testing autentikasi
    test_user = User(username='testuser')
    test_user.set_password('testpassword')
    session.add(test_user)
    session.commit()

    def teardown():
        transaction.abort()
        Base.metadata.drop_all(engine) # Hapus skema DB setelah tes
        session.close()

    request.addfinalizer(teardown)
    return session

# Header autentikasi dasar untuk tes
def basic_auth_header(username, password):
    import base64
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('ascii')
    return {'Authorization': f'Basic {token}'}

# --- Tes untuk CRUD Items ---
def test_get_items_empty(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    res = testapp.get('/api/v1/items', headers=headers, status=200)
    assert res.json == {'items': []}

def test_create_item_success(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    payload = {'name': 'Test Item 1', 'description': 'A test item'}
    res = testapp.post_json('/api/v1/items', payload, headers=headers, status=201) # HTTP 201 Created
    assert res.json['message'] == 'Item created successfully'
    assert res.json['item']['name'] == 'Test Item 1'
    assert 'id' in res.json['item']

    # Verifikasi item ada di DB
    item_id = res.json['item']['id']
    item_in_db = db_session.query(Item).get(item_id)
    assert item_in_db is not None
    assert item_in_db.name == 'Test Item 1'

def test_create_item_missing_name(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    payload = {'description': 'A test item without name'}
    testapp.post_json('/api/v1/items', payload, headers=headers, status=400) # HTTP 400 Bad Request

def test_get_one_item_success(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    # Buat item dulu
    item1 = Item(name='Item to Get', description='Details')
    db_session.add(item1)
    db_session.commit()

    res = testapp.get(f'/api/v1/items/{item1.id}', headers=headers, status=200)
    assert res.json['item']['name'] == 'Item to Get'
    assert res.json['item']['id'] == item1.id

def test_get_one_item_not_found(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    testapp.get('/api/v1/items/9999', headers=headers, status=404) # HTTP 404 Not Found

def test_update_item_success(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    item1 = Item(name='Original Name', description='Original Desc')
    db_session.add(item1)
    db_session.commit()

    update_payload = {'name': 'Updated Name', 'description': 'Updated Desc'}
    res = testapp.put_json(f'/api/v1/items/{item1.id}', update_payload, headers=headers, status=200)
    assert res.json['message'] == 'Item updated successfully'
    assert res.json['item']['name'] == 'Updated Name'

    # Verifikasi di DB
    updated_item = db_session.query(Item).get(item1.id)
    assert updated_item.name == 'Updated Name'

def test_delete_item_success(testapp, db_session):
    headers = basic_auth_header('testuser', 'testpassword')
    item1 = Item(name='To Be Deleted', description='Delete me')
    db_session.add(item1)
    db_session.commit()
    item_id = item1.id

    testapp.delete(f'/api/v1/items/{item_id}', headers=headers, status=204) # HTTP 204 No Content

    # Verifikasi di DB
    deleted_item = db_session.query(Item).get(item_id)
    assert deleted_item is None

# --- Tes untuk Autentikasi ---
def test_get_items_unauthorized(testapp, db_session):
    # Tanpa header autentikasi
    testapp.get('/api/v1/items', status=401) # HTTP 401 Unauthorized

def test_create_item_unauthorized(testapp, db_session):
    payload = {'name': 'Test Item Unauth', 'description': 'Should fail'}
    testapp.post_json('/api/v1/items', payload, status=401)

def test_register_user_success(testapp, db_session):
    payload = {'username': 'newuser', 'password': 'newpassword'}
    res = testapp.post_json('/api/v1/auth/register', payload, status=201)
    assert res.json['message'] == 'User registered successfully'

    # Verifikasi user ada di DB (password sudah di-hash)
    user_in_db = db_session.query(User).filter_by(username='newuser').first()
    assert user_in_db is not None
    assert user_in_db.check_password('newpassword')

def test_register_user_duplicate_username(testapp, db_session):
    # User 'testuser' sudah dibuat di fixture db_session
    payload = {'username': 'testuser', 'password': 'anotherpassword'}
    testapp.post_json('/api/v1/auth/register', payload, status=400) # HTTP 400 Bad Request