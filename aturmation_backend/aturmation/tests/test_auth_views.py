import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPUnauthorized, HTTPBadRequest
import json
from ..models.user import User
from .base import BaseTest


class AuthViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add a test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        self.session.add(self.user)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_login_success(self):
        from ..views.auth import AuthView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'username': 'testuser',
                'password': 'password'
            }
        )
        request.auth_policy = self.config.registry.getUtility(
            self.config.registry._auths[0].__class__
        )
        
        view = AuthView(request)
        response = view.login()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertIn('token', body)
        self.assertIn('user', body)
        self.assertEqual(body['user']['username'], 'testuser')
    
    def test_login_invalid_credentials(self):
        from ..views.auth import AuthView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        request.auth_policy = self.config.registry.getUtility(
            self.config.registry._auths[0].__class__
        )
        
        view = AuthView(request)
        response = view.login()
        
        self.assertEqual(response.status_code, 401)
        body = json.loads(response.body)
        self.assertIn('error', body)
    
    def test_register_success(self):
        from ..views.auth import AuthView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'newpassword'
            }
        )
        request.auth_policy = self.config.registry.getUtility(
            self.config.registry._auths[0].__class__
        )
        
        view = AuthView(request)
        response = view.register()
        
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.body)
        self.assertIn('token', body)
        self.assertIn('user', body)
        self.assertEqual(body['user']['username'], 'newuser')
        
        # Check that user was created in database
        user = self.session.query(User).filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')
    
    def test_register_existing_username(self):
        from ..views.auth import AuthView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'username': 'testuser',  # Existing username
                'email': 'another@example.com',
                'password': 'newpassword'
            }
        )
        request.auth_policy = self.config.registry.getUtility(
            self.config.registry._auths[0].__class__
        )
        
        view = AuthView(request)
        response = view.register()
        
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertIn('error', body)
        self.assertIn('username', body['error'])
