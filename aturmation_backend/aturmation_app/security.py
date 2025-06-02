# aturmation_app/security.py
import os
import datetime
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
    Allow,
)
import jwt
from jwt.exceptions import PyJWTError

# Tetap gunakan JWT_SECRET untuk enkripsi token
JWT_SECRET = os.environ.get('JWT_SECRET', 'ganti-dengan-kunci-rahasia-anda-yang-kuat!')
JWT_ALGORITHM = 'HS256'

def create_jwt_token(user_id, username):
    """Buat JWT token tanpa menyertakan role"""
    payload = {
        'sub': str(user_id),
        'username': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    """Verifikasi JWT token"""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError as e:
        print(f"[DEBUG security.py - verify_jwt_token] JWT verification failed: {str(e)}")
        return None

class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    """Token-based Authentication Policy using JWT."""
    def __init__(self, callback=None):
        self.callback = callback

    def unauthenticated_userid(self, request):
        """Extract user ID from JWT token in the Authorization header."""
        jwt_token = self._get_jwt_token(request)
        if not jwt_token:
            return None
        
        payload = verify_jwt_token(jwt_token)
        if payload is None:
            return None
            
        return payload.get('sub')
    
    def remember(self, request, userid, **kw):
        """No-op since JWT tokens are stateless."""
        return []
        
    def forget(self, request):
        """Returns HTTP headers to forget the current user."""
        return [('Authorization', '')]
        
    def _get_jwt_token(self, request):
        """Extract JWT token from Authorization header."""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header:
            return None
            
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
            
        return parts[1]

class RootACL:
    """Simplified ACL that gives all authenticated users full access."""
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
        (Allow, Authenticated, 'delete'),
    ]
    
    def __init__(self, request):
        pass

def get_user(request):
    """Get current user from request."""
    user_id = request.unauthenticated_userid
    if user_id is not None:
        from .models import User
        return request.dbsession.query(User).filter(User.id == user_id).first()
    return None

def includeme(config):
    # Set authentication and authorization policies
    authn_policy = JWTAuthenticationPolicy()
    config.set_authentication_policy(authn_policy)
    
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    
    # Get JWT secret from settings if available
    settings = config.get_settings()
    global JWT_SECRET
    JWT_SECRET = settings.get('jwt.secret', JWT_SECRET)
    
    # Add request methods
    config.add_request_method(get_user, 'user', reify=True)
    
    # Set default root factory
    config.set_root_factory(RootACL)