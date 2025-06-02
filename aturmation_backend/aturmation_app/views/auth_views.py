import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPNotFound
import sqlalchemy.exc

from ..models import User
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
    
    try:
        # Create new user (role tidak perlu diatur - akan menggunakan default 'user')
        user = User(name=name, username=username, email=email)
        user.set_password(password)
        
        request.dbsession.add(user)
        log.debug("auth_register_view: User object added to session. Attempting flush...")
        request.dbsession.flush()  # To get the ID
        log.debug("auth_register_view: Session flushed successfully. User ID should be available.")
        
        # Create and return JWT token (tanpa role)
        token = create_jwt_token(user.id, user.username)
        log.debug("auth_register_view: JWT token created.")
        
        return Response(json_body={
            'status': 'success',
            'message': 'Registration successful',
            'token': token,
            'user': user.to_dict()
        }, status=201)
    except sqlalchemy.exc.IntegrityError as e:
        log.error(f"auth_register_view: IntegrityError - {e}")
        request.dbsession.rollback()
        return Response(json_body={
            'status': 'error', 
            'message': 'Database error occurred'
        }, status=500)

@view_config(route_name='api_auth_login', request_method='POST', renderer='json')
def auth_login_view(request):
    """Login a user"""
    try:
        data = request.json_body
    except ValueError:
        return Response(json_body={'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return Response(json_body={
            'status': 'error', 
            'message': 'Both username and password are required'
        }, status=400)
    
    user = request.dbsession.query(User).filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return Response(json_body={
            'status': 'error', 
            'message': 'Invalid username or password'
        }, status=401)
    
    # Create and return JWT token (tanpa role)
    token = create_jwt_token(user.id, user.username)
    
    return Response(json_body={
        'status': 'success',
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })

@view_config(route_name='api_auth_me', permission='view', renderer='json')
def auth_me_view(request):
    """Get the current authenticated user"""
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
