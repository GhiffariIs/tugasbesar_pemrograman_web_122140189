from pyramid.config import Configurator
from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import basic_auth_check # Impor fungsi check yang baru

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Konfigurasi autentikasi dasar
        authn_policy = BasicAuthAuthenticationPolicy(check=basic_auth_check) # Gunakan basic_auth_check
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        # Include routes
        config.include('aturmation_backend.routes')
        
        # Scan for view classes
        config.scan('aturmation_backend.views')
    return config.make_wsgi_app()