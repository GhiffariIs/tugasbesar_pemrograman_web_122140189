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

PROFILE_EDIT_PERMISSION = 'profile:edit' 

@view_config(
    route_name='api_user_profile_update',
    request_method='PUT',
    renderer='json',
    permission=PROFILE_EDIT_PERMISSION
)
def update_user_profile_view(request):
    user_id = request.authenticated_userid # ID user yang sedang login (dari token JWT)
    if not user_id:
        # Seharusnya tidak terjadi jika permission 'Authenticated' sudah dicek
        raise HTTPForbidden(json_body={'message': 'Authentication required.'})

    try:
        print(f"[DEBUG] update_user_profile_view: Attempting to update profile for user ID: {user_id}")
        user_to_update = request.dbsession.query(User).get(user_id)

        if not user_to_update:
            # Skenario aneh jika user_id dari token valid tapi user tidak ada di DB
            raise HTTPNotFound(json_body={'message': 'User not found.'})

        data = request.json_body
        print(f"[DEBUG] update_user_profile_view: Received data: {data}")

        updated_fields = []
        errors = {}

        # Update Name
        if 'name' in data:
            new_name = data.get('name')
            if not new_name or not isinstance(new_name, str) or len(new_name.strip()) == 0:
                errors['name'] = 'Name must be a non-empty string.'
            elif len(new_name) > 100:
                errors['name'] = 'Name cannot exceed 100 characters.'
            else:
                user_to_update.name = new_name
                updated_fields.append('name')
        
        # Update Email
        if 'email' in data:
            new_email = data.get('email')
            if not new_email or not isinstance(new_email, str) or len(new_email.strip()) == 0: # Basic check
                errors['email'] = 'Email must be a non-empty string.'
            # TODO: Tambahkan validasi format email yang lebih baik
            elif len(new_email) > 100:
                errors['email'] = 'Email cannot exceed 100 characters.'
            else:
                # Cek apakah email baru sudah digunakan oleh user lain
                if new_email.lower() != user_to_update.email.lower(): # Hanya cek jika email diubah
                    existing_user_with_email = request.dbsession.query(User).filter(
                        User.email == new_email,
                        User.id != user_id # Abaikan user saat ini
                    ).first()
                    if existing_user_with_email:
                        errors['email'] = f"Email '{new_email}' is already in use by another account."
                    else:
                        user_to_update.email = new_email
                        updated_fields.append('email')
                else: # Email sama, tidak ada perubahan
                    pass 
        
        # Update Photo URL (untuk sekarang hanya sebagai string)
        if 'photo' in data:
            # Frontend mengirimkan URL string untuk foto
            # Validasi sederhana: apakah itu string dan tidak terlalu panjang
            new_photo_url = data.get('photo')
            if new_photo_url is not None: # Boleh string kosong atau null untuk menghapus foto
                if not isinstance(new_photo_url, str):
                     errors['photo'] = 'Photo URL must be a string.'
                elif len(new_photo_url) > 255: # Sesuaikan panjang maksimal jika perlu
                     errors['photo'] = 'Photo URL is too long.'
                else:
                    user_to_update.photo = new_photo_url if new_photo_url.strip() else None # Set None jika string kosong
                    updated_fields.append('photo')
            else: # Jika dikirim null, artinya hapus foto
                user_to_update.photo = None
                updated_fields.append('photo')


        if errors:
            raise HTTPBadRequest(json_body={'message': 'Validation failed.', 'errors': errors})

        if not updated_fields:
            return HTTPOk(json_body={
                'message': 'No changes detected or no valid fields provided for update.',
                'user': user_to_update.as_dict()
            })

        # request.dbsession.add(user_to_update) # Tidak perlu jika sudah di-track sesi
        request.dbsession.flush() # Untuk menjalankan validasi DB dan error lebih awal
        print(f"[DEBUG] update_user_profile_view: Profile updated for user ID {user_id}. Fields: {', '.join(updated_fields)}")
        
        return HTTPOk(json_body={
            'message': 'Profile updated successfully.',
            'user': user_to_update.as_dict()
        })

    except HTTPBadRequest as e:
        # request.dbsession.rollback() # pyramid_tm akan handle rollback
        return e
    except IntegrityError as e: # Jika ada unique constraint (misal email) yang terlewat validasi
        request.dbsession.rollback()
        print(f"[DEBUG] update_user_profile_view: IntegrityError - {e}")
        # Cek apakah error karena email duplikat
        if 'uq_users_email' in str(e).lower() or ('unique constraint' in str(e).lower() and 'email' in str(e).lower()):
             return HTTPBadRequest(json_body={'message': 'Profile update failed.', 'errors': {'email': f"Email '{data.get('email')}' is already in use."}})
        return HTTPBadRequest(json_body={'message': 'Profile update failed due to a data conflict.'})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_user_profile_view: DBAPIError - {e}")
        return HTTPBadRequest(json_body={'message': "Database error during profile update."})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_user_profile_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})