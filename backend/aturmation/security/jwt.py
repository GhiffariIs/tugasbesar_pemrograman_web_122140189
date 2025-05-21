import jwt
from datetime import datetime, timedelta
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Everyone, Allow, Deny


def get_user(request):
    user_id = request.authenticated_userid
    if user_id:
        return request.dbsession.query(request.registry.User).filter_by(id=user_id).first()
    return None


class MyAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, settings):
        self.jwt_secret = settings['jwt.secret']
        self.jwt_algorithm = settings.get('jwt.algorithm', 'HS256')
        self.jwt_expiration = int(settings.get('jwt.expiration', 3600))
        
    def authenticated_userid(self, request):
        token = self._get_token(request)
        if token:
            try:
                payload = jwt.decode(
                    token, 
                    self.jwt_secret, 
                    algorithms=[self.jwt_algorithm]
                )
                user_id = payload.get('sub')
                if user_id:
                    return user_id
            except jwt.PyJWTError:
                return None
        return None
    
    def generate_token(self, user_id):
        """Generate a new JWT token for a user."""
        payload = {
            'sub': user_id,  # Subject
            'iat': datetime.utcnow(),  # Issued at
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiration)  # Expiration
        }
        return jwt.encode(
            payload, 
            self.jwt_secret, 
            algorithm=self.jwt_algorithm
        )
    
    def unauthenticated_userid(self, request):
        return self.authenticated_userid(request)
    
    def callback(self, userid, request):
        if userid:
            user = request.dbsession.query(request.registry.User).filter_by(id=userid).first()
            if user:
                return ['group:admin'] if user.is_admin else ['group:user']
        return None
    
    def _get_token(self, request):
        """Extract token from request."""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]  # Remove 'Bearer ' prefix
        return None


class RootFactory:
    """Define ACL (Access Control List) for different routes."""
    __acl__ = [
        (Allow, 'group:admin', 'admin'),
        (Allow, Authenticated, 'user'),
        (Deny, Everyone, 'admin'),
    ]

    def __init__(self, request):
        self.request = request


def includeme(config):
    settings = config.get_settings()
    
    # Add authentication
    authn_policy = MyAuthenticationPolicy(settings)
    authz_policy = ACLAuthorizationPolicy()
    
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    # Make the authentication policy available as request.auth_policy
    config.add_request_method(
        lambda request: request.registry.getUtility(MyAuthenticationPolicy), 
        'auth_policy', 
        reify=True
    )
    
    # Add the get_user method to the request
    config.add_request_method(get_user, 'user', reify=True)