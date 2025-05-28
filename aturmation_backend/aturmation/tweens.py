"""CORS handling tween"""

def cors_tween_factory(handler, registry):
    """Create a CORS tween."""
    
    settings = registry.settings
    
    # Get allowed origins from settings
    allowed_origins = settings.get('cors.origins', 'http://localhost:5173')
    if isinstance(allowed_origins, str):
        allowed_origins = [o.strip() for o in allowed_origins.split(' ')]
        
    def cors_tween(request):
        """The CORS tween handles Cross-Origin Resource Sharing."""
        
        # Handle OPTIONS preflight request
        if request.method == 'OPTIONS':
            response = request.response
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                'Access-Control-Max-Age': '3600'
            })
            return response
            
        # Process the request normally
        response = handler(request)
        
        # Add CORS headers to all responses
        origin = request.headers.get('Origin', '')
        if origin in allowed_origins or '*' in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            response.headers['Access-Control-Allow-Origin'] = allowed_origins[0] if allowed_origins else '*'
            
        # Additional CORS headers
        response.headers.update({
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'
        })
            
        return response
        
    return cors_tween
