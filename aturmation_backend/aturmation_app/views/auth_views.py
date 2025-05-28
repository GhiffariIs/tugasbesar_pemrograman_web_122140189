from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPCreated, HTTPOk, HTTPUnauthorized
from sqlalchemy.exc import IntegrityError, DBAPIError # Tambahkan DBAPIError di sini

from ..models.user import User, UserRole
from ..security import create_jwt_token  # Pastikan Anda memiliki fungsi ini untuk membuat token JWT

@view_config(route_name='api_register', request_method='POST', renderer='json')
def auth_register_view(request):
    try:
        print("[DEBUG] auth_register_view: Attempting to get JSON body...") # DEBUG BARU
        data = request.json_body
        print(f"[DEBUG] auth_register_view: Received JSON body (data): {data}") # DEBUG BARU - Lihat isi 'data'

        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # DEBUG BARU - Lihat nilai individual setelah .get()
        print(f"[DEBUG] auth_register_view: name='{name}', username='{username}', email='{email}', password='{password is not None}'") 

        if not all([name, username, email, password]):
            print("[DEBUG] auth_register_view: Validation failed - one or more required fields are missing/empty.") # DEBUG BARU
            # Berikan detail field mana yang kosong untuk debugging
            missing_fields = []
            if not name: missing_fields.append("name")
            if not username: missing_fields.append("username")
            if not email: missing_fields.append("email")
            if not password: missing_fields.append("password")
            print(f"[DEBUG] auth_register_view: Missing or empty fields: {', '.join(missing_fields)}")

            raise HTTPBadRequest(json_body={'message': f"Fields are required: {', '.join(missing_fields)}."}) # Pesan lebih spesifik

        # ... (sisa kode untuk membuat User, dll.)
        # Jika sampai sini, berarti validasi di atas lolos
        print("[DEBUG] auth_register_view: Basic validation passed. Proceeding to create user.")

        new_user = User(
            name=name,
            username=username,
            email=email,
            role=UserRole.staff
        )
        new_user.set_password(password)

        request.dbsession.add(new_user)
        print("[DEBUG] auth_register_view: User object added to session. Attempting flush...")
        request.dbsession.flush() 
        print("[DEBUG] auth_register_view: Session flushed successfully. User ID should be available.")

        token = create_jwt_token(new_user.id, new_user.username, new_user.role)
        print("[DEBUG] auth_register_view: JWT token created.")

        return HTTPCreated(json_body={
            'message': 'User registered successfully.',
            'token': token,
            'user': new_user.as_dict()
        })

    # ... (blok except lainnya tetap sama) ...
    except IntegrityError: 
        request.dbsession.rollback()
        # ... (logika cek duplikat username/email) ...
        print("[DEBUG] auth_register_view: IntegrityError caught.") # DEBUG BARU
        existing_user_by_username = request.dbsession.query(User).filter_by(username=username).first()
        if existing_user_by_username:
             return HTTPBadRequest(json_body={'message': 'Username already exists.'})
        existing_user_by_email = request.dbsession.query(User).filter_by(email=email).first()
        if existing_user_by_email:
             return HTTPBadRequest(json_body={'message': 'Email already exists.'})
        return HTTPBadRequest(json_body={'message': 'User registration failed due to a conflict.'})
    except DBAPIError:
        request.dbsession.rollback()
        print("[DEBUG] auth_register_view: DBAPIError caught.") # DEBUG BARU
        return Response("Database error during registration.", content_type='text/plain', status=500)
    except ValueError: 
        print("[DEBUG] auth_register_view: ValueError caught (likely bad JSON format).") # DEBUG BARU
        return HTTPBadRequest(json_body={'message': 'Invalid JSON format in request body.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] auth_register_view: Unexpected Exception caught: {type(e).__name__} - {e}") # DEBUG BARU
        # print full traceback for unexpected errors
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", content_type='text/plain', status=500)

@view_config(route_name='api_auth_login', request_method='POST', renderer='json')
def auth_login_view(request):
    try:
        data = request.json_body
        username = data.get('username') # Frontend mengirim 'username'
        password = data.get('password')

        print(f"[DEBUG] auth_login_view: Attempting login for username='{username}', password_present='{password is not None}'")

        if not username or not password:
            print("[DEBUG] auth_login_view: Username or password missing.")
            raise HTTPBadRequest(json_body={'message': 'Username and password are required.'})

        user = request.dbsession.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            print(f"[DEBUG] auth_login_view: Login successful for user: {username}")
            token = create_jwt_token(user.id, user.username, user.role)
            return HTTPOk(json_body={ # Menggunakan HTTPOk untuk respons 200 OK
                'message': 'Login successful.',
                'token': token,
                'user': user.as_dict()
            })
        else:
            print(f"[DEBUG] auth_login_view: Invalid username or password for: {username}")
            return HTTPUnauthorized(json_body={'message': 'Invalid username or password.'})
            
    except ValueError: # Gagal parse JSON body
        print("[DEBUG] auth_login_view: ValueError (likely bad JSON format).")
        return HTTPBadRequest(json_body={'message': 'Invalid JSON format in request body.'})
    except Exception as e:
        print(f"[DEBUG] auth_login_view: Unexpected Exception caught: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred during login: {e}", content_type='text/plain', status=500)


@view_config(route_name='api_auth_me', request_method='GET', renderer='json', permission='view_authenticated') # Tambahkan permission
def auth_me_view(request):
    # user_id didapat dari token JWT melalui JWTAuthenticationPolicy yang memanggil get_principals
    user_id = request.authenticated_userid 
    
    print(f"[DEBUG] auth_me_view: authenticated_userid from token: {user_id}")

    if user_id:
        user = request.dbsession.query(User).get(user_id)
        if user:
            print(f"[DEBUG] auth_me_view: User found for id {user_id}: {user.username}")
            return user.as_dict() # Kembalikan data user
        else:
            print(f"[DEBUG] auth_me_view: User not found in DB for id {user_id}, though token was valid for this id.")
            # Ini skenario aneh, token valid tapi user tidak ada di DB.
            return HTTPUnauthorized(json_body={'message': 'User associated with token not found.'})
            
    print("[DEBUG] auth_me_view: No authenticated_userid found. Denying access or token invalid.")
    # Jika user_id tidak ada (token tidak valid, tidak ada token, atau get_principals gagal)
    # Pyramid akan menangani ini berdasarkan permission='view_authenticated' dan ACL.
    # Biasanya akan menghasilkan 401 atau 403. Kita bisa return 401 secara eksplisit jika mau.
    return HTTPUnauthorized(json_body={'message': 'Authentication required.'})