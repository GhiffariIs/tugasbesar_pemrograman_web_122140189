from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPCreated
from sqlalchemy.exc import IntegrityError, DBAPIError # Tambahkan DBAPIError di sini

from ..models.user import User

@view_config(route_name='api_register', request_method='POST', renderer='json')
def register_user(request):
    try:
        data = request.json_body
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise HTTPBadRequest("Username and password are required")

        # Cek apakah username sudah ada
        existing_user = request.dbsession.query(User).filter_by(username=username).first()
        if existing_user:
            raise HTTPBadRequest("Username already exists")

        new_user = User(username=username)
        new_user.set_password(password) # Hash password
        request.dbsession.add(new_user)
        # request.dbsession.flush() # Tidak perlu flush jika tidak langsung butuh ID
        return HTTPCreated(json_body={'message': 'User registered successfully'})
    except IntegrityError: # Jika ada unique constraint violation (meskipun sudah dicek)
        request.dbsession.rollback()
        return HTTPBadRequest("Username already exists or other integrity error.")
    except DBAPIError:
        request.dbsession.rollback()
        return Response("Database error", content_type='text/plain', status=500)
    except ValueError as e: # Jika json_body gagal parse
        return HTTPBadRequest(str(e))

# Endpoint untuk login (opsional, karena kita pakai Basic Auth)
# Jika ingin endpoint login terpisah untuk mendapatkan token (misalnya JWT),
# maka ini perlu diimplementasikan. Untuk Basic Auth, klien mengirim kredensial di setiap request.

# @view_config(route_name='api_login_check', request_method='GET', renderer='json', permission='view')
# def login_check(request):
#     # Jika request ini berhasil, berarti autentikasi (Basic Auth) berhasil
#     return {'message': 'Authentication successful', 'user_id': request.authenticated_userid}