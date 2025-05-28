"""
View initialization
"""
from pyramid.view import view_config

@view_config(route_name='api_home', renderer='json')
def api_home(request):
    """API home."""
    return {
        'status': 'success',
        'message': 'Welcome to the Aturmation API',
        'version': '0.1'
    }
