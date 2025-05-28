import unittest
import transaction
from pyramid import testing
from ..models.user import User
from .base import BaseTest


class UserModelTest(BaseTest):
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        self.session.add(user)
        self.session.flush()
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.password_hash)
        self.assertFalse(user.is_admin)
        
    def test_password_verification(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        self.session.add(user)
        self.session.flush()
        
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('wrongpassword'))
        
    def test_to_dict(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        self.session.add(user)
        self.session.flush()
        
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertFalse(user_dict['is_admin'])
        self.assertNotIn('password_hash', user_dict)
