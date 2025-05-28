"""Tests for authentication views."""
import json
import jwt
from datetime import datetime
import pytest
from pyramid.testing import DummyRequest

from aturmation.views.auth import login, register, current_user
from aturmation.models.user import User

def test_login_success(app_settings, db_session, monkeypatch):
    """Test successful login."""
    # Create a test user
    user = User(
        username='loginuser',
        email='login@example.com',
        name='Login User',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    # Create a request with JSON body
    request = DummyRequest(
        json_body={
            'username': 'loginuser',
            'password': 'password'
        }
    )
    request.dbsession = db_session
    
    # Add settings to registry
    class Registry:
        settings = app_settings
    
    request.registry = Registry()
    
    # Mock the create_jwt_token function
    def mock_create_jwt_token(user, request):
        return 'fake-token'
    
    monkeypatch.setattr('aturmation.views.auth.create_jwt_token', mock_create_jwt_token)
    
    # Call the login view
    result = login(request)
    
    assert 'token' in result
    assert result['token'] == 'fake-token'
    assert 'user' in result
    assert result['user']['username'] == 'loginuser'

def test_login_invalid_credentials(db_session):
    """Test login with invalid credentials."""
    # Create a test user
    user = User(
        username='badlogin',
        email='badlogin@example.com',
        name='Bad Login',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    # Create a request with wrong password
    request = DummyRequest(
        json_body={
            'username': 'badlogin',
            'password': 'wrongpassword'
        }
    )
    request.dbsession = db_session
    
    # Call the login view
    result = login(request)
    
    assert result.status_code == 401
    response_json = json.loads(result.body.decode())
    assert response_json['status'] == 'error'
    assert 'Invalid username or password' in response_json['message']

def test_register_success(app_settings, db_session, monkeypatch):
    """Test successful registration."""
    # Create a request with JSON body
    request = DummyRequest(
        json_body={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'password'
        }
    )
    request.dbsession = db_session
    
    # Add settings to registry
    class Registry:
        settings = app_settings
    
    request.registry = Registry()
    
    # Mock the create_jwt_token function
    def mock_create_jwt_token(user, request):
        return 'fake-token'
    
    monkeypatch.setattr('aturmation.views.auth.create_jwt_token', mock_create_jwt_token)
    
    # Call the register view
    result = register(request)
    
    assert 'token' in result
    assert result['token'] == 'fake-token'
    assert 'user' in result
    assert result['user']['username'] == 'newuser'
    assert result['user']['email'] == 'newuser@example.com'
    assert result['user']['name'] == 'New User'
    assert result['user']['role'] == 'staff'
    
    # Check that the user was saved to the database
    user = User.by_username('newuser', db_session)
    assert user is not None
    assert user.email == 'newuser@example.com'

def test_register_duplicate_username(db_session):
    """Test registration with duplicate username."""
    # Create a test user
    user = User(
        username='existinguser',
        email='existing@example.com',
        name='Existing User',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    # Create a request with duplicate username
    request = DummyRequest(
        json_body={
            'username': 'existinguser',  # Already exists
            'email': 'different@example.com',
            'name': 'Different User',
            'password': 'password'
        }
    )
    request.dbsession = db_session
    
    # Call the register view
    result = register(request)
    
    assert result.status_code == 400
    response_json = json.loads(result.body.decode())
    assert response_json['status'] == 'error'
    assert 'Username already exists' in response_json['message']

def test_current_user(db_session):
    """Test current_user view."""
    # Create a test user
    user = User(
        username='currentuser',
        email='current@example.com',
        name='Current User',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    # Create a request with authenticated user
    request = DummyRequest()
    request.user = user
    request.dbsession = db_session
    
    # Call the current_user view
    result = current_user(request)
    
    assert result['id'] == user.id
    assert result['username'] == 'currentuser'
    assert result['email'] == 'current@example.com'
    assert result['name'] == 'Current User'
    assert result['role'] == 'staff'
