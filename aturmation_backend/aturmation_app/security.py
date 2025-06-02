# aturmation_app/security.py
import os
import jwt
from datetime import datetime, timedelta, timezone
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import (
    ACLAuthorizationPolicy, 
    Allow,
    Deny, # Mungkin tidak terpakai jika kita hanya Allow
    Everyone,
    Authenticated,
    ALL_PERMISSIONS # Mungkin tidak terpakai jika kita spesifik
)
from pyramid.interfaces import IAuthenticationPolicy
from zope.interface import implementer

from .models.user import User, UserRole

# Default secret yang akan diganti dalam includeme()
JWT_SECRET = 'ganti-dengan-kunci-rahasia-anda-yang-kuat!'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600 * 24 

def create_jwt_token(user_id, username, role):
    print(f"[DEBUG create_jwt_token] Creating token for user: {username}, role: {role}")
    print(f"[DEBUG create_jwt_token] Using JWT_SECRET: {JWT_SECRET[:5]}...")
    payload = {
        'sub': str(user_id),
        'user_id': user_id, 'username': username, 
        'role': role.value if isinstance(role, UserRole) else str(role),
        'exp': datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(f"[DEBUG create_jwt_token] Token created: {token[:20]}...")
    return token

def verify_jwt_token(token):
    try:
        print(f"[DEBUG verify_jwt_token] Using JWT_SECRET: {JWT_SECRET[:5]}...")
        print(f"[DEBUG verify_jwt_token] Attempting to verify token: {token[:20]}...")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"[DEBUG verify_jwt_token] Token verified successfully: {decoded.get('username')}")
        return decoded
    except jwt.ExpiredSignatureError:
        print("[DEBUG verify_jwt_token] Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[DEBUG verify_jwt_token] Invalid token: {str(e)}")
        return None
    except jwt.PyJWTError as e:
        print(f"[DEBUG verify_jwt_token] JWT verification failed: {e}")
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
    def get_token(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer': return parts[1]
        return None
    def remember(self, request, userid, **kw): return [] 
    def forget(self, request): return [] 

def get_principals(userid, request):
    if userid:
        user = request.dbsession.query(User).get(userid) 
        if user:
            role_value = user.role.value if user.role else 'unknown_role'
            principals = [Authenticated, f'user:{user.id}', f'role:{role_value}']
            print(f"[DEBUG security.py - get_principals] User ID: {userid}, Role: {role_value}, Principals: {principals}")
            return principals
    print(f"[DEBUG security.py - get_principals] No userid ({userid}) or user not found. Returning None.")
    return None

class RootACL(object):
    __acl__ = [
        (Allow, Authenticated, 'view_authenticated'), # Untuk /auth/me
        (Allow, Authenticated, 'profile:edit'),     # Untuk update profil sendiri

        # Permissions untuk PRODUCTS - semua user adalah admin
        (Allow, f'role:{UserRole.admin.value}', 'product:view'),
        (Allow, f'role:{UserRole.admin.value}', 'product:add'),
        (Allow, f'role:{UserRole.admin.value}', 'product:edit'),
        (Allow, f'role:{UserRole.admin.value}', 'product:delete')
    ]
    def __init__(self, request): self.request = request

def includeme(config):
    settings = config.get_settings()
    global JWT_SECRET
    new_secret = settings.get('jwt.secret')
    if new_secret:
        JWT_SECRET = new_secret
        print(f"[DEBUG includeme] JWT_SECRET updated from settings: {JWT_SECRET[:5]}...")
    else:
        print(f"[DEBUG includeme] Using default JWT_SECRET: {JWT_SECRET[:5]}...")
    
    authn_policy = JWTAuthenticationPolicy(callback=get_principals)
    authz_policy = ACLAuthorizationPolicy() 
    
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootACL)