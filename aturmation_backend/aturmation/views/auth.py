from pyramid.view import view_config
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden

from ..models import DBSession
from ..models.user import User
from ..security import create_jwt_token
from .base import BaseView

@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    """Login view."""
    try:
        body = request.json_body
        username = body.get('username')
        password = body.get('password')
        
        if not username or not password:
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Username and password are required'
            })
        
        user = User.by_username(username, DBSession)
        if not user or not user.check_password(password):
            return HTTPUnauthorized(json_body={
                'status': 'error',
                'message': 'Invalid username or password'
            })
        
        token = create_jwt_token(user, request)
        
        return {
            'token': token,
            'user': user.to_dict()
        }
    except Exception as e:
        return HTTPBadRequest(json_body={
            'status': 'error',
            'message': str(e)
        })

@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    """Register view."""
    try:
        body = request.json_body
        username = body.get('username')
        email = body.get('email')
        name = body.get('name')
        password = body.get('password')
        
        if not username or not email or not name or not password:
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'All fields are required'
            })
        
        # Check if username already exists
        if User.by_username(username, DBSession):
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Username already exists'
            })
        
        # Check if email already exists
        if User.by_email(email, DBSession):
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Email already exists'
            })
        
        # Create user
        user = User(
            username=username,
            email=email,
            name=name,
            role='staff'  # Default role
        )
        user.set_password(password)
        
        DBSession.add(user)
        DBSession.flush()
        
        token = create_jwt_token(user, request)
        
        return {
            'token': token,
            'user': user.to_dict()
        }
    except Exception as e:
        return HTTPBadRequest(json_body={
            'status': 'error',
            'message': str(e)
        })

@view_config(route_name='me', request_method='GET', renderer='json', permission='view')
def current_user(request):
    """Current user view."""
    user = request.user
    
    if not user:
        return HTTPUnauthorized(json_body={
            'status': 'error',
            'message': 'Not authenticated'
        })
    
    return user.to_dict()
