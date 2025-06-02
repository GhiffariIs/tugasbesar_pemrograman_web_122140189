# aturmation_app/__init__.py
from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.events import NewRequest
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    
    try:
        with Configurator(settings=settings) as config:
            # Include basic components
            config.include('pyramid_jinja2')
            config.include('.models')
            config.include('.routes')
            
            # Konfigurasi CORS
            def add_cors_headers_response_callback(event):
                def cors_headers(request, response):
                    response.headers.update({
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
                        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Max-Age': '1728000',
                    })
                event.request.add_response_callback(cors_headers)
            
            config.add_subscriber(add_cors_headers_response_callback, NewRequest)
            
            # Tambahkan tween untuk manajemen session database
            config.add_tween('aturmation_app.tweens.db_session_tween_factory')
            
            # Konfigurasi JSON renderer
            json_renderer = JSON()
            config.add_renderer('json', json_renderer)
            
            # Konfigurasi security
            from .security import JWTAuthenticationPolicy, RootFactory
            from pyramid.authorization import ACLAuthorizationPolicy
            
            # Set up authentication
            authn_policy = JWTAuthenticationPolicy()
            authz_policy = ACLAuthorizationPolicy()
            config.set_authentication_policy(authn_policy)
            config.set_authorization_policy(authz_policy)
            config.set_root_factory(RootFactory)
            
            # Tambahkan security request methods
            config.add_request_method('.security.get_user', 'user', reify=True)
            
            # Scan views
            config.scan()
            
            return config.make_wsgi_app()
            
    except Exception as e:
        logger.error(f"Error in initialization: {e}", exc_info=True)
        raise