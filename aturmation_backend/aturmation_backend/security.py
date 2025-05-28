from pyramid.security import Authenticated, Allow, Deny, Everyone
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import remember, forget
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a security policy
def get_security_policy():
    return BasicAuthAuthenticationPolicy(check_credentials)

def get_authorization_policy():
    return ACLAuthorizationPolicy()

# Hardcoded credentials for testing
USERS = {'editor': 'editor_password',
         'viewer': 'viewer_password'}
GROUPS = {'editor': ['group:editors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
    return None

# Function to check user credentials
def check_credentials(username, password):
    # Here you would typically fetch the user from the database
    user = get_user_from_db(username)
    if user and pwd_context.verify(password, user.password):
        return user
    return None

# Function to hash a password
def hash_password(password):
    return pwd_context.hash(password)

# Function to get user from the database (placeholder)
def get_user_from_db(username):
    # This function should interact with the database to retrieve the user
    pass

# Define the ACL for the application
def get_acl():
    return [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit'),
        (Deny, Authenticated, 'delete'),
    ]

# Simplified Basic Auth check function
def basic_auth_check(username, password, request):
    """Pemeriksa untuk Basic Authentication."""
    expected_username = request.registry.settings.get('auth.username', 'your_username')
    expected_password = request.registry.settings.get('auth.password', 'your_password')

    if username == expected_username and password == expected_password:
        return ['user:' + username] # Sederhanakan untuk saat ini
    return None