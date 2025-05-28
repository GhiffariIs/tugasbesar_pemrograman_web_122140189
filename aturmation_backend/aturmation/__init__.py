from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated, Everyone
import os
import logging

logger = logging.getLogger(__name__)

class Root:
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'role:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

def includeme(config):
    # Configuration packages to include
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')

def main(global_config, **settings):
    """Main application factory"""
    with Configurator(settings=settings) as config:
        # Authentication & Authorization
        config.include('.security')
        config.set_root_factory(Root)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        
        # Include components
        includeme(config)
        
        # Cross-Origin Resource Sharing (CORS) configuration
        config.add_tween('aturmation.tweens.cors_tween_factory')
        
        # Static assets
        config.add_static_view('static', 'static', cache_max_age=3600)
        
        # Scan for view configuration
        config.scan()
        
        return config.make_wsgi_app()
