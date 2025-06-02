# aturmation_app/tweens.py
from pyramid.settings import aslist
import logging
from pyramid.response import Response

log = logging.getLogger(__name__)

def cors_tween_factory(handler, registry):
    """
    Tween untuk menangani CORS secara lebih komprehensif
    """
    def cors_tween(request):
        # Jika ini adalah OPTIONS request (preflight)
        if request.method == 'OPTIONS':
            response = Response()
            response.headers.update({
                'Access-Control-Allow-Origin': 'http://localhost:5173',
                'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '1728000',
            })
            return response
            
        # Untuk request non-OPTIONS, proses seperti biasa
        response = handler(request)
        
        # Tambahkan header CORS ke semua respons
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
        
        return response
        
    return cors_tween

def db_session_tween_factory(handler, registry):
    """
    Tween factory untuk mengelola session database.
    Melakukan commit jika request berhasil, rollback jika ada exception.
    """
    def db_session_tween(request):
        try:
            # Process the request
            response = handler(request)
            
            # If there's a database session, commit changes
            if hasattr(request, 'dbsession'):
                try:
                    request.dbsession.commit()
                except Exception as e:
                    log.error(f"Error committing database session: {e}")
                    request.dbsession.rollback()
                    raise
            
            return response
        except Exception:
            # If there's an exception, rollback any changes
            if hasattr(request, 'dbsession'):
                request.dbsession.rollback()
            raise
        finally:
            # Close the session
            if hasattr(request, 'dbsession'):
                request.dbsession.close()
    
    return db_session_tween