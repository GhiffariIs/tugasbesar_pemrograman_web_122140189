import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPInternalServerError

import sqlalchemy.exc

from ..models import User
from ..models.user import UserRole
from ..security import create_jwt_token

log = logging.getLogger(__name__)

@view_config(route_name='api_auth_register', request_method='POST', renderer='json')
def auth_register_view(request):
    """Register a new user"""
    log.debug("auth_register_view: Attempting to get JSON body...")
    try:
        data = request.json_body
        log.debug(f"auth_register_view: Received JSON body (data): {data}")
    except ValueError:
        return Response(json_body={'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        log.error(f"Unexpected error getting JSON body: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred'
        })
    
    # Extract data
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    log.debug(f"auth_register_view: name='{name}', username='{username}', email='{email}', password='{bool(password)}'")
    
    # Basic validation
    if not all([name, username, email, password]):
        return Response(json_body={
            'status': 'error', 
            'message': 'Missing required fields'
        }, status=400)
    
    try:
        # Check if username already exists
        if request.dbsession.query(User).filter_by(username=username).first():
            return Response(json_body={
                'status': 'error', 
                'message': 'Username already exists'
            }, status=400)
        
        # Check if email already exists
        if request.dbsession.query(User).filter_by(email=email).first():
            return Response(json_body={
                'status': 'error', 
                'message': 'Email already registered'
            }, status=400)
        
        log.debug("auth_register_view: Basic validation passed. Proceeding to create user.")
        
        # Create new user with staff role
        user = User(name=name, username=username, email=email)
        user.set_password(password)
        user.role = UserRole.STAFF  # Use UserRole enum
        
        request.dbsession.add(user)
        request.dbsession.flush()  # To get the ID
        log.debug(f"auth_register_view: Session flushed successfully. User ID: {user.id}")
        
        # Create and return JWT token
        token = create_jwt_token(user.id, user.username)
        log.debug("auth_register_view: JWT token created successfully.")
        
        return Response(json_body={
            'status': 'success',
            'message': 'Registration successful',
            'token': token,
            'user': user.to_dict()
        }, status=201)
    except sqlalchemy.exc.IntegrityError as e:
        log.error(f"auth_register_view: IntegrityError - {e}")
        return Response(json_body={
            'status': 'error', 
            'message': 'Database error occurred'
        }, status=500)
    except Exception as e:
        log.error(f"auth_register_view: Unexpected error - {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'An unexpected error occurred'
        })

@view_config(route_name='api_auth_login', request_method='POST', renderer='json')
def auth_login_view(request):
    """Login a user"""
    try:
        data = request.json_body
        log.debug(f"auth_login_view: Received JSON body: {data}")
    except ValueError:
        log.warning("auth_login_view: Invalid JSON")
        return Response(json_body={'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        log.error(f"auth_login_view: Unexpected error getting JSON - {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred'
        })
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return Response(json_body={
            'status': 'error', 
            'message': 'Both username and password are required'
        }, status=400)
    
    try:
        user = request.dbsession.query(User).filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            log.warning(f"auth_login_view: Invalid login attempt for username '{username}'")
            return Response(json_body={
                'status': 'error', 
                'message': 'Invalid username or password'
            }, status=401)
        
        # Create and return JWT token
        token = create_jwt_token(user.id, user.username)
        log.debug(f"auth_login_view: Login successful for '{username}'")
        
        return Response(json_body={
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
    except Exception as e:
        log.error(f"auth_login_view: Error - {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred'
        })

@view_config(route_name='api_auth_me', permission='view', renderer='json')
def auth_me_view(request):
    """Get the current authenticated user"""
    try:
        user = request.user
        if not user:
            return Response(json_body={
                'status': 'error',
                'message': 'Not authenticated'
            }, status=401)
        
        return Response(json_body={
            'status': 'success',
            'user': user.to_dict()
        })
    except Exception as e:
        log.error(f"auth_me_view: Error - {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred'
        })
