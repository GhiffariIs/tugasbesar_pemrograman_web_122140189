from pyramid.view import view_defaults, view_config
from pyramid.response import Response
import json
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPForbidden,
    HTTPUnauthorized,
)

class BaseView:
    """Base class for all views"""
    
    def __init__(self, request):
        self.request = request
        self.dbsession = request.dbsession
    
    def json_response(self, data, status=200):
        """Return a JSON response"""
        body = json.dumps(data)
        return Response(
            body=body,
            status=status,
            content_type='application/json'
        )
    
    def error_response(self, message, status=400):
        """Return an error response"""
        return self.json_response({'error': message}, status=status)
