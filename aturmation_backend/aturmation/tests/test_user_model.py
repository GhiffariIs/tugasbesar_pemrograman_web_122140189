"""Tests for the user model."""
import pytest
import bcrypt
from aturmation.models.user import User

def test_user_init(db_session):
    """Test that a user can be created."""
    user = User(
        username='testuser',
        email='test@example.com',
        name='Test User',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.name == 'Test User'
    assert user.role == 'staff'
    assert user.password_hash is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    
def test_user_password(db_session):
    """Test password hashing and checking."""
    user = User(
        username='passworduser',
        email='password@example.com',
        name='Password User',
        role='staff'
    )
    user.set_password('testpassword')
    db_session.add(user)
    db_session.flush()
    
    # Password should be hashed, not stored as plaintext
    assert user.password_hash != 'testpassword'
    
    # Check password should work with correct password
    assert user.check_password('testpassword') is True
    
    # Check password should fail with incorrect password
    assert user.check_password('wrongpassword') is False
    
def test_user_is_admin(db_session):
    """Test is_admin property."""
    admin_user = User(
        username='admin_user',
        email='admin@example.com',
        name='Admin User',
        role='admin'
    )
    staff_user = User(
        username='staff_user',
        email='staff@example.com',
        name='Staff User',
        role='staff'
    )
    db_session.add(admin_user)
    db_session.add(staff_user)
    db_session.flush()
    
    assert admin_user.is_admin is True
    assert staff_user.is_admin is False
    
def test_user_to_dict(db_session):
    """Test to_dict method."""
    user = User(
        username='dictuser',
        email='dict@example.com',
        name='Dict User',
        role='staff'
    )
    user.set_password('password')
    db_session.add(user)
    db_session.flush()
    
    user_dict = user.to_dict()
    assert user_dict['id'] == user.id
    assert user_dict['username'] == 'dictuser'
    assert user_dict['email'] == 'dict@example.com'
    assert user_dict['name'] == 'Dict User'
    assert user_dict['role'] == 'staff'
    assert 'password_hash' not in user_dict
    assert 'created_at' in user_dict
    
def test_user_by_username(db_session):
    """Test by_username class method."""
    user = User(
        username='finduser',
        email='find@example.com',
        name='Find User',
        role='staff'
    )
    db_session.add(user)
    db_session.flush()
    
    found_user = User.by_username('finduser', db_session)
    assert found_user is user
    
    not_found_user = User.by_username('nonexistentuser', db_session)
    assert not_found_user is None
    
def test_user_by_email(db_session):
    """Test by_email class method."""
    user = User(
        username='emailuser',
        email='emailtest@example.com',
        name='Email User',
        role='staff'
    )
    db_session.add(user)
    db_session.flush()
    
    found_user = User.by_email('emailtest@example.com', db_session)
    assert found_user is user
    
    not_found_user = User.by_email('nonexistent@example.com', db_session)
    assert not_found_user is None
    
def test_user_validate_email(db_session):
    """Test email validation."""
    # Valid email
    user = User(
        username='validemail',
        email='valid@example.com',
        name='Valid Email',
        role='staff'
    )
    db_session.add(user)
    db_session.flush()
    
    # Invalid email should raise an assertion error
    with pytest.raises(AssertionError):
        user = User(
            username='invalidemail',
            email='invalidemail',
            name='Invalid Email',
            role='staff'
        )
        db_session.add(user)
        db_session.flush()
        
def test_user_validate_username(db_session):
    """Test username validation."""
    # Valid username (>=3 characters)
    user = User(
        username='validuser',
        email='validuser@example.com',
        name='Valid User',
        role='staff'
    )
    db_session.add(user)
    db_session.flush()
    
    # Invalid username (too short) should raise an assertion error
    with pytest.raises(AssertionError):
        user = User(
            username='ab',  # Too short
            email='shortuser@example.com',
            name='Short User',
            role='staff'
        )
        db_session.add(user)
        db_session.flush()
