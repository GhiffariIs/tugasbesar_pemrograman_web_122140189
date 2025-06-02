# aturmation_app/security.py
import os
import datetime
import jwt
import logging
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
    Allow,
)

log = logging.getLogger(__name__)

# JWT settings
JWT_SECRET = 'aturmation-secret-key'  # Idealnya dari settings
JWT_ALGORITHM = 'HS256'

def create_jwt_token(user_id, username):
    """Create a JWT token for authentication"""
    try:
        payload = {
            'sub': str(user_id),
            'username': username,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        # JWT library returns bytes in some versions, string in others
        if isinstance(token, bytes):
            return token.decode('utf-8')
        return token
    except Exception as e:
        log.error(f"Error creating JWT token: {e}")
        raise

def parse_jwt_token(token):
    """Parse a JWT token and return the payload"""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        log.warning("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        log.warning(f"Invalid token: {e}")
        return None
    except Exception as e:
        log.error(f"Unexpected error parsing token: {e}")
        return None

def get_user(request):
    """Get the current user from the request"""
    # Avoid circular imports
    from .models import User
    
    # PENTING: Periksa apakah ini adalah request untuk /api/v1/auth/me
    # untuk mencegah rekursi tak terhingga
    if request.path == '/api/v1/auth/me' and hasattr(request, '_get_user_recursion'):
        return None
    
    # Set flag untuk menghindari rekursi
    request._get_user_recursion = True
    
    # Check if user is already in request (menggunakan nama yang berbeda untuk menghindari konflik)
    cached_user = getattr(request, '_cached_user', None)
    if cached_user is not None:
        return cached_user
    
    # Extract token from header
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ', 1)[1]
    payload = parse_jwt_token(token)
    if payload is None:
        return None
    
    user_id = payload.get('sub')
    if not user_id:
        return None
    
    # Get user from database
    try:
        user = request.dbsession.query(User).filter_by(id=user_id).first()
        if user:
            # Store user in request to avoid multiple database lookups
            # Gunakan nama yang berbeda untuk menghindari konflik
            request._cached_user = user
        return user
    except Exception as e:
        log.error(f"Error getting user from database: {e}")
        return None

class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    def unauthenticated_userid(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ', 1)[1]
        payload = parse_jwt_token(token)
        if payload is None:
            return None
            
        return payload.get('sub')
    
    def callback(self, userid, request):
        # Simplified for testing - all authenticated users get all permissions
        if userid:
            return ['view', 'create', 'edit', 'delete']
        return []

# Root factory to define ACLs
class RootFactory(object):
    """Root factory for ACL"""
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
        (Allow, Authenticated, 'delete'),
    ]
    
    def __init__(self, request):
        pass