import jwt
from datetime import datetime, timedelta, timezone
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ( # GANTI KE INI
    ACLAuthorizationPolicy, Allow, Deny, Everyone, Authenticated, ALL_PERMISSIONS
)
from pyramid.interfaces import IAuthenticationPolicy
from zope.interface import implementer

from .models.user import User, UserRole

JWT_SECRET = 'ganti-dengan-kunci-rahasia-anda-yang-kuat!' # AMBIL DARI SETTINGS NANTI
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600 * 24 # 1 hari

def create_jwt_token(user_id, username, role):
    payload = {
        'user_id': user_id, 
        'username': username, 
        'role': role.value if isinstance(role, UserRole) else str(role), # Pastikan role adalah string
        'exp': datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(f"[DEBUG security.py - verify_jwt_token] JWT verification failed: {e}")
        return None

@implementer(IAuthenticationPolicy)
class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback=None): 
        self.callback = callback
    
    def unauthenticated_userid(self, request):
        token = self.get_token(request)
        if token:
            payload = verify_jwt_token(token)
            if payload: 
                return payload.get('user_id')
        return None

    # authenticated_userid adalah alias untuk unauthenticated_userid di versi Pyramid lebih baru
    # dan tidak perlu diimplementasikan secara eksplisit jika unauthenticated_userid sudah ada.
    # def authenticated_userid(self, request):
    #     return self.unauthenticated_userid(request)

    def get_token(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer': 
                return parts[1]
        return None
    
    def remember(self, request, userid, **kw): return [] 
    def forget(self, request): return [] 

def get_principals(userid, request):
    if userid:
        # Pastikan request.dbsession tersedia dan berfungsi dengan baik dalam konteks tes
        # Jika DBSession global dikonfigurasi dengan benar di conftest.py untuk pyramid_app,
        # maka request.dbsession (yang disediakan oleh pyramid_tm) akan menggunakan engine tes.
        user = request.dbsession.query(User).get(userid) 
        if user:
            role_value = user.role.value if user.role else 'unknown_role'
            principals_to_return = [Authenticated, f'user:{user.id}', f'role:{role_value}']
            print(f"[DEBUG security.py - get_principals] User ID: {userid}, Role: {role_value}, Principals: {principals_to_return}")
            return principals_to_return
    print(f"[DEBUG security.py - get_principals] No userid ({userid}) or user not found. Returning None.")
    return None

class RootACL(object):
    __acl__ = [
        (Allow, Authenticated, 'view_authenticated'),
        (Allow, f'role:{UserRole.admin.value}', 'admin_action'), 
        
        (Allow, f'role:{UserRole.admin.value}', 'category:view'),
        (Allow, f'role:{UserRole.admin.value}', 'category:add'),
        (Allow, f'role:{UserRole.admin.value}', 'category:edit'),
        (Allow, f'role:{UserRole.admin.value}', 'category:delete'),
        (Allow, f'role:{UserRole.staff.value}', 'category:view'),
        (Allow, f'role:{UserRole.staff.value}', 'category:add'),

        (Allow, f'role:{UserRole.admin.value}', 'product:view'),
        (Allow, f'role:{UserRole.admin.value}', 'product:add'),
        (Allow, f'role:{UserRole.admin.value}', 'product:edit'),
        (Allow, f'role:{UserRole.admin.value}', 'product:delete'),
        (Allow, f'role:{UserRole.staff.value}', 'product:view'),
        (Allow, f'role:{UserRole.staff.value}', 'product:add'),
        (Allow, f'role:{UserRole.staff.value}', 'product:edit'),

        (Allow, f'role:{UserRole.admin.value}', 'transaction:view'),
        (Allow, f'role:{UserRole.admin.value}', 'transaction:add'),
        (Allow, f'role:{UserRole.staff.value}', 'transaction:view'),
        (Allow, f'role:{UserRole.staff.value}', 'transaction:add'),

        (Allow, f'role:{UserRole.admin.value}', 'dashboard:view'),
        (Allow, f'role:{UserRole.staff.value}', 'dashboard:view'),
        
        (Allow, Authenticated, 'profile:edit'),
    ]
    def __init__(self, request): 
        self.request = request

def includeme(config):
    settings = config.get_settings()
    global JWT_SECRET # Pastikan JWT_SECRET adalah variabel global jika diubah di sini
    new_secret = settings.get('jwt.secret')
    if new_secret: # Hanya update jika ada di settings
        JWT_SECRET = new_secret
    
    authn_policy = JWTAuthenticationPolicy(callback=get_principals)
    # ACLAuthorizationPolicy diimpor dari pyramid.authorization
    authz_policy = ACLAuthorizationPolicy() 
    
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootACL)