from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny, Everyone, Authenticated
from passlib.context import CryptContext

from .models.user import User # Pastikan path import benar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi untuk mendapatkan user dari database berdasarkan username
def get_user(username, request):
    # Tambahkan print di sini untuk memastikan fungsi ini dipanggil
    print(f"[DEBUG] get_user called for: {username}")
    user = request.dbsession.query(User).filter_by(username=username).first()
    if user:
        print(f"[DEBUG] User found: {user.username}")
    else:
        print(f"[DEBUG] User NOT found: {username}")
    return user

# Callback untuk BasicAuthAuthenticationPolicy
def basic_auth_check(username, password, request):
    print(f"\n[DEBUG] basic_auth_check called with username: '{username}', password: '{password}'") # Debug 1
    user = get_user(username, request)
    if user:
        print(f"[DEBUG] User object retrieved for {username}: {user}") # Debug 2
        password_check_result = user.check_password(password)
        print(f"[DEBUG] user.check_password('{password}') result: {password_check_result}") # Debug 3
        if password_check_result:
            principals = [f'user:{user.id}', 'g:user']
            print(f"[DEBUG] Authentication SUCCESSFUL for {username}. Principals returned: {principals}") # Debug 4
            return principals
        else:
            print(f"[DEBUG] Password check FAILED for {username}.") # Debug 5
    else:
        print(f"[DEBUG] User {username} not found in database during auth check.") # Debug 6

    print(f"[DEBUG] Authentication FAILED for {username}. Returning None.") # Debug 7
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