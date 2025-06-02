# tests/test_auth_api.py
from aturmation_app.models import UserRole # Pastikan UserRole diimpor dari models Anda

# Fixtures seperti testapp, create_test_user, auth_token_for_user
# akan otomatis tersedia jika didefinisikan dengan benar di tests/conftest.py.

def test_login_success(testapp, auth_token_for_user):
    """Test successful login, JWT token generation, and then test /me."""
    test_username = "loginsuccess_user_v2" # Gunakan username yang unik untuk tes ini
    test_password = "password123"
    user_name = "Login Success User v2"
    user_email = "loginsuccess_v2@example.com" # Pastikan email unik

    # auth_token_for_user akan membuat user jika belum ada dan melakukan login
    # serta melakukan commit agar user terlihat oleh testapp
    jwt_token = auth_token_for_user(
        username=test_username,
        password=test_password,
        name=user_name,
        email=user_email,
        role=UserRole.staff # Menggunakan UserRole Enum
    )
    assert jwt_token is not None, "Token should be generated on successful login"

    # Uji endpoint /auth/me menggunakan token ini
    headers = {'Authorization': f'Bearer {jwt_token}'}
    me_res = testapp.get('/api/v1/auth/me', headers=headers, status=200)
    
    assert me_res.json['username'] == test_username
    assert me_res.json['name'] == user_name
    assert me_res.json['email'] == user_email
    assert me_res.json['role'] == UserRole.staff.value # Verifikasi role value (string)

def test_login_failure_wrong_password(testapp, create_test_user):
    """Test login failure with wrong password."""
    test_username = "wrongpass_user_v2" # Username unik
    test_password = "correctpassword"
    
    # Buat user tes. create_test_user dari conftest.py akan commit jika diminta.
    create_test_user(
        name="Wrong Pass User v2",
        username=test_username,
        email="wrongpass_v2@example.com", # Pastikan email unik
        password=test_password,
        role=UserRole.staff,
        commit_session=True # Penting agar user ini ada di DB untuk testapp
    )

    login_payload = {"username": test_username, "password": "thisisawrongpassword"}
    res = testapp.post_json('/api/v1/auth/login', login_payload, status=401) 
    
    assert 'message' in res.json, "Response should contain a message key"
    assert res.json['message'] == 'Invalid username or password.'

def test_login_failure_user_not_found(testapp):
    """Test login failure for a non-existent user."""
    login_payload = {"username": "iamverynonexistentuser", "password": "anypassword"}
    res = testapp.post_json('/api/v1/auth/login', login_payload, status=401)
    
    assert 'message' in res.json, "Response should contain a message key"
    assert res.json['message'] == 'Invalid username or password.'

# TODO (Tambahkan tes-tes ini selanjutnya):
# def test_register_user_success(testapp):
#     """Test successful user registration."""
#     # ... (payload untuk user baru yang unik) ...
#     # res = testapp.post_json('/api/v1/auth/register', payload, status=201)
#     # assert 'token' in res.json
#     # assert 'user' in res.json
#     # assert res.json['user']['username'] == payload['username']
#     pass

# def test_register_user_duplicate_username(testapp, create_test_user):
#     """Test registration failure with duplicate username."""
#     # ... (buat user dulu dengan create_test_user) ...
#     # ... (coba registrasi lagi dengan username yang sama) ...
#     # res = testapp.post_json('/api/v1/auth/register', payload, status=400)
#     # assert 'Username already exists' in res.json['message']
#     pass

# def test_register_user_duplicate_email(testapp, create_test_user):
#     """Test registration failure with duplicate email."""
#     # ... (buat user dulu dengan create_test_user) ...
#     # ... (coba registrasi lagi dengan email yang sama) ...
#     # res = testapp.post_json('/api/v1/auth/register', payload, status=400)
#     # assert 'Email already exists' in res.json['message']
#     pass

# def test_auth_me_no_token(testapp):
#     """Test /auth/me endpoint without a token."""
#     # res = testapp.get('/api/v1/auth/me', status=[401, 403]) # Bergantung pada bagaimana Pyramid menangani
#     pass

# def test_auth_me_invalid_token(testapp):
#     """Test /auth/me endpoint with an invalid token."""
#     # headers = {'Authorization': 'Bearer invalidtoken123'}
#     # res = testapp.get('/api/v1/auth/me', headers=headers, status=[401, 403])
#     pass