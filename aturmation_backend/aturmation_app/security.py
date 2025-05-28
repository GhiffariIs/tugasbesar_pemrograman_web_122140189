from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny, Everyone, Authenticated
from passlib.context import CryptContext

from .models.user import User # Pastikan path import benar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi untuk mendapatkan user dari database berdasarkan username
def get_user(username, request):
    return request.dbsession.query(User).filter_by(username=username).first()

# Callback untuk BasicAuthAuthenticationPolicy
def basic_auth_check(username, password, request):
    user = get_user(username, request)
    if user and user.check_password(password):
        # Kembalikan daftar principals jika autentikasi berhasil
        # 'g:user' adalah contoh group, bisa disesuaikan
        return [f'user:{user.id}', 'g:user']
    return None

class RootACL(object):
    # Default: Semua orang bisa melihat (GET)
    # Hanya user terautentikasi yang bisa membuat, mengubah, menghapus
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, Authenticated, 'edit'),
        (Allow, Authenticated, 'delete'),
        (Deny, Everyone, 'create'), # Eksplisit deny untuk yang tidak terautentikasi
        (Deny, Everyone, 'edit'),
        (Deny, Everyone, 'delete'),
    ]

    def __init__(self, request):
        self.request = request

def includeme(config):
    settings = config.get_settings()
    authn_policy = BasicAuthAuthenticationPolicy(check=basic_auth_check)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(RootACL)