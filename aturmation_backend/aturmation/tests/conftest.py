"""Test configuration"""
import pytest
import transaction
from pyramid import testing
from pyramid.paster import get_appsettings
import webtest

from aturmation import main
from aturmation.models import Base, DBSession

@pytest.fixture(scope='session')
def app_settings():
    """Get application settings."""
    settings = get_appsettings('test.ini')
    settings['sqlalchemy.url'] = 'sqlite:///:memory:'
    return settings

@pytest.fixture(scope='session')
def app(app_settings):
    """Create test application."""
    return main({}, **app_settings)

@pytest.fixture(scope='session')
def testapp(app):
    """Create test app."""
    return webtest.TestApp(app)

@pytest.fixture(scope='session')
def init_database(app_settings):
    """Initialize test database."""
    from sqlalchemy import create_engine
    engine = create_engine(app_settings['sqlalchemy.url'])
    Base.metadata.create_all(engine)
    
    DBSession.configure(bind=engine)
    
    # Create test data
    with transaction.manager:
        from aturmation.models.user import User
        admin = User(
            username='admin',
            name='Administrator',
            email='admin@aturmation.com',
            role='admin'
        )
        admin.set_password('admin123')
        DBSession.add(admin)
        
        staff = User(
            username='staff',
            name='Staff Demo',
            email='staff@aturmation.com',
            role='staff'
        )
        staff.set_password('staff123')
        DBSession.add(staff)
    
    yield DBSession
    
    # Cleanup
    Base.metadata.drop_all(engine)
    DBSession.remove()

@pytest.fixture(scope='function')
def db_session(init_database):
    """Create a new db session for each test."""
    with transaction.manager:
        yield init_database
        transaction.abort()
        
@pytest.fixture
def dummy_request(db_session):
    """Create a dummy request."""
    request = testing.DummyRequest()
    request.dbsession = db_session
    return request
