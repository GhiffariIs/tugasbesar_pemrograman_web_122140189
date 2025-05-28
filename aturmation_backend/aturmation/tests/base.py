"""Base test class configuration"""

import unittest
import transaction

from pyramid import testing
from pyramid.paster import get_appsettings
import webtest

from ..models import Base, DBSession

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = get_appsettings('test.ini')
        cls.settings['sqlalchemy.url'] = 'sqlite:///:memory:'

    def setUp(self):
        self.config = testing.setUp(settings=self.settings)
        self.config.include('..models')
        
        from sqlalchemy import create_engine
        engine = create_engine(self.settings['sqlalchemy.url'])
        Base.metadata.create_all(engine)
        
        DBSession.configure(bind=engine)
        
    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

class FunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from aturmation import main
        cls.settings = get_appsettings('test.ini')
        cls.settings['sqlalchemy.url'] = 'sqlite:///:memory:'
        app = main({}, **cls.settings)
        cls.testapp = webtest.TestApp(app)
        
        from sqlalchemy import create_engine
        engine = create_engine(cls.settings['sqlalchemy.url'])
        Base.metadata.create_all(engine)
        
        # Create admin user
        with transaction.manager:
            from ..models.user import User
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
    
    def setUp(self):
        pass
        
    def tearDown(self):
        DBSession.remove()
        
    @classmethod
    def tearDownClass(cls):
        DBSession.remove()
