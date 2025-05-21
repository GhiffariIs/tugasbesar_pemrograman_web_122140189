from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.session import SignedCookieSessionFactory
import datetime
import enum
from .models.user import User

def add_cors_headers_response_callback(event):
    """Add CORS headers to all responses."""
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

def handle_options_request(request):
    """Handle preflight OPTIONS requests."""
    response = request.response
    if 'Access-Control-Request-Headers' in request.headers:
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        request.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
    return response

def json_datetime_adapter(obj, request):
    """Convert datetime objects to ISO format strings for JSON."""
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def json_enum_adapter(obj, request):
    """Convert enum objects to strings for JSON."""
    return obj.value if isinstance(obj, enum) else obj

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Configure JSON renderer to handle datetime and enum objects
        json_renderer = JSON()
        json_renderer.add_adapter(datetime.datetime, json_datetime_adapter)
        json_renderer.add_adapter(enum.Enum, json_enum_adapter)
        config.add_renderer('json', json_renderer)
        
        # Configure session
        session_factory = SignedCookieSessionFactory(
            settings.get('session.secret', 'aturmation-secret')
        )
        config.set_session_factory(session_factory)
        
        # Include packages
        config.include('pyramid_tm')
        config.include('cornice')
        
        # Include our routes and models
        config.include('.models')
        config.include('.routes')
        config.include('.security.jwt')
        
        # Add User to registry for authentication policy
        config.registry.User = User
        
        # CORS configuration
        config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewResponse')
        config.add_route('cors_preflight', '/{catch_all:.*}', request_method="OPTIONS")
        config.add_view(handle_options_request, route_name='cors_preflight')
        
        # Add a special method to config object
        config.add_cors_preflight_handler = lambda: None
        
        # Scan the package for views
        config.scan()
        
        return config.make_wsgi_app()