from pyramid.security import NO_PERMISSION_REQUIRED
from .security.jwt import RootFactory

def includeme(config):
    """Define routes for our application."""
    
    # Set up our custom root factory for all routes
    config.set_root_factory(RootFactory)
    
    # Authentication routes
    config.add_route('login', '/api/login', permission=NO_PERMISSION_REQUIRED)
    config.add_route('register', '/api/register', permission=NO_PERMISSION_REQUIRED)
    config.add_route('logout', '/api/logout')
    config.add_route('user_info', '/api/user')
    config.add_route('auth', '/api/auth')
    
    # Category routes
    config.add_route('categories', '/api/categories')
    config.add_route('category', '/api/categories/{id}')
    
    # Product routes
    config.add_route('products', '/api/products')
    config.add_route('product', '/api/products/{id}')
    
    # Transaction routes
    config.add_route('transactions', '/api/transactions')
    config.add_route('transaction', '/api/transactions/{id}')