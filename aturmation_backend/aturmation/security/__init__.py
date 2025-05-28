from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated
import jwt
import datetime

def get_user(request):
    """Get the user from the request."""
    user_id = request.unauthenticated_userid
    if user_id is not None:
        from ..models import DBSession
        from ..models.user import User
        return DBSession.query(User).get(user_id)
    return None

def get_jwt_token(request):
    """Get the JWT token from the request."""
    authorization = request.headers.get('Authorization')
    if not authorization:
        return None
        
    try:
        scheme, token = authorization.strip().split(' ', 1)
        if scheme.lower() != 'bearer':
            return None
        return token
    except ValueError:
        return None

def parse_jwt_token(token, request):
    """Parse and validate the JWT token."""
    if token is None:
        return None
        
    try:
        settings = request.registry.settings
        secret = settings.get('jwt.secret')
        algorithm = settings.get('jwt.algorithm', 'HS256')
        
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        user_id = payload.get('sub')
        return user_id
    except jwt.InvalidTokenError:
        return None

class JWTAuthenticationPolicy:
    """JWT Authentication policy."""
    
    def __init__(self, settings):
        self.secret = settings.get('jwt.secret', 'secret')
        self.algorithm = settings.get('jwt.algorithm', 'HS256')
        self.expiration = int(settings.get('jwt.expiration', 3600))
        
    def authenticated_userid(self, request):
        """Return the authenticated userid or None."""
        token = get_jwt_token(request)
        return parse_jwt_token(token, request)
        
    def unauthenticated_userid(self, request):
        """Return the unauthenticated userid or None."""
        token = get_jwt_token(request)
        return parse_jwt_token(token, request)
        
    def effective_principals(self, request):
        """Return a list of principals."""
        principals = [Everyone]
        user_id = self.authenticated_userid(request)
        
        if user_id:
            principals.append(Authenticated)
            principals.append(f'user:{user_id}')
            
            # Add roles
            user = get_user(request)
            if user:
                principals.append(f'role:{user.role}')
                
        return principals
        
    def remember(self, request, userid, **kw):
        """Create a JWT token."""
        return []
        
    def forget(self, request):
        """Clear the token."""
        return []

def create_jwt_token(user, request):
    """Create a JWT token for the user."""
    settings = request.registry.settings
    secret = settings.get('jwt.secret', 'secret')
    algorithm = settings.get('jwt.algorithm', 'HS256')
    expiration = int(settings.get('jwt.expiration', 3600))
    
    payload = {
        'sub': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    }
    
    return jwt.encode(payload, secret, algorithm=algorithm)

def includeme(config):
    """Include the security settings."""
    settings = config.get_settings()
    
    # JWT Authentication
    authentication_policy = JWTAuthenticationPolicy(settings)
    authorization_policy = ACLAuthorizationPolicy()
    
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    
    # Add the request.user property
    config.add_request_method(get_user, 'user', reify=True)
