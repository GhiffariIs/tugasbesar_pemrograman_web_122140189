import jwt
from datetime import datetime, timedelta, timezone
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from zope.interface import implementer
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
    Authenticated,
    ALL_PERMISSIONS
)
from .models.user import User, UserRole
# from .models import DBSession # Tidak perlu jika pakai request.dbsession di get_principals

JWT_SECRET = 'ganti-dengan-kunci-rahasia-anda-yang-kuat!' # AMBIL DARI SETTINGS NANTI
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600 * 24 # 1 hari

def create_jwt_token(user_id, username, role):
    payload = {
        'user_id': user_id, 'username': username, 'role': role.value if isinstance(role, UserRole) else role,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@implementer(IAuthenticationPolicy)
class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback=None): self.callback = callback
    def unauthenticated_userid(self, request):
        token = self.get_token(request)
        if token:
            payload = verify_jwt_token(token)
            if payload: return payload.get('user_id')
        return None
    def get_token(self, request): # (Implementasi get_token dari header Authorization: Bearer)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer': return parts[1]
        return None
    # remember & forget bisa dikosongkan untuk JWT stateless
    def remember(self, request, userid, **kw): return []
    def forget(self, request): return []


def get_principals(userid, request):
    if userid:
        user = request.dbsession.query(User).get(userid)
        if user:
            role_value = user.role.value if user.role else 'unknown_role'
            principals_to_return = [Authenticated, f'user:{user.id}', f'role:{role_value}']
            # TAMBAHKAN ATAU PASTIKAN PRINT INI ADA:
            print(f"[DEBUG security.py - get_principals] User ID: {userid}, Role: {role_value}, Principals: {principals_to_return}")
            return principals_to_return
    print(f"[DEBUG security.py - get_principals] No userid or user not found for ID {userid}. Returning None.")
    return None
    
class RootACL(object):
    __acl__ = [
        # Permissions untuk Autentikasi & User Umum
        (Allow, Authenticated, 'view_authenticated'), # Untuk endpoint /auth/me

        # --- Permissions untuk CATEGORIES ---
        (Allow, f'role:{UserRole.admin.value}', 'category:view'),
        (Allow, f'role:{UserRole.admin.value}', 'category:add'),
        (Allow, f'role:{UserRole.admin.value}', 'category:edit'),
        (Allow, f'role:{UserRole.admin.value}', 'category:delete'),
        
        # Staff hanya boleh melihat dan menambah kategori (contoh)
        (Allow, f'role:{UserRole.staff.value}', 'category:view'),
        (Allow, f'role:{UserRole.staff.value}', 'category:add'),

        # Admin boleh semua untuk produk
        (Allow, f'role:{UserRole.admin.value}', 'product:view'),
        (Allow, f'role:{UserRole.admin.value}', 'product:add'),
        (Allow, f'role:{UserRole.admin.value}', 'product:edit'),
        (Allow, f'role:{UserRole.admin.value}', 'product:delete'),
        
        # Staff boleh lihat, tambah, dan edit produk (contoh)
        (Allow, f'role:{UserRole.staff.value}', 'product:view'),
        (Allow, f'role:{UserRole.staff.value}', 'product:add'),
        (Allow, f'role:{UserRole.staff.value}', 'product:edit'),

        # TODO: Tambahkan ACL untuk Products dan entitas lain di sini nanti
    ]

    def __init__(self, request):
        self.request = request

def includeme(config):
    settings = config.get_settings()
    global JWT_SECRET
    JWT_SECRET = settings.get('jwt.secret', JWT_SECRET)
    authn_policy = JWTAuthenticationPolicy(callback=get_principals)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootACL)