from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPUnauthorized,
    HTTPForbidden
)
import json

class BaseView:
    """Base view class with common functionality."""
    
    def __init__(self, request):
        self.request = request
        self.db = request.dbsession
        
    def _get_json_body(self):
        """Get the request body as JSON."""
        try:
            return self.request.json_body
        except json.JSONDecodeError:
            raise HTTPBadRequest('Invalid JSON')
    
    def _json_response(self, data):
        """Return a JSON response."""
        self.request.response.headers['Content-Type'] = 'application/json'
        return json.dumps(data)
        
    def _error_response(self, message, status_code=400):
        """Return an error response."""
        self.request.response.status_code = status_code
        return self._json_response({
            'status': 'error',
            'message': message
        })
