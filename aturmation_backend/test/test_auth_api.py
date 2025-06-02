# tests/test_auth_api.py
import pytest # Tidak perlu jika tidak ada mark atau fixture khusus di file ini

# Impor model jika perlu membuat data tes di dalam fungsi tes
# from aturmation_app.models import User, UserRole

# Fixtures seperti testapp, db_session, create_test_user, auth_token_for_user
# akan otomatis tersedia jika ada di conftest.py atau diimpor.

def test_login_success(testapp, create_test_user, db_session):
    """Test successful login and JWT token generation."""
    # 1. Buat user tes di database
    test_username = "logintestuser"
    test_password = "password123"
    create_test_user(
        name="Login Test User",
        username=test_username,
        email="login@example.com",
        password=test_password,
        role="staff", # atau UserRole.staff
        save=True # Pastikan user disimpan
    )
    # db_session.commit() # Jika create_test_user tidak auto-commit

    # 2. Lakukan request login
    login_payload = {"username": test_username, "password": test_password}
    res = testapp.post_json('/api/v1/auth/login', login_payload, status=200)

    # 3. Verifikasi respons
    assert 'token' in res.json
    assert 'user' in res.json
    assert res.json['user']['username'] == test_username
    assert res.json['message'] == 'Login successful.'
    
    # Verifikasi token (opsional, tapi bagus)
    # Anda bisa mencoba decode token di sini menggunakan JWT_SECRET tes jika mau,
    # atau langsung gunakan token ini untuk tes endpoint terproteksi.
    jwt_token = res.json['token']
    
    # 4. Uji endpoint /auth/me menggunakan token ini
    headers = {'Authorization': f'Bearer {jwt_token}'}
    me_res = testapp.get('/api/v1/auth/me', headers=headers, status=200)
    assert me_res.json['username'] == test_username

def test_login_failure_wrong_password(testapp, create_test_user, db_session):
    """Test login failure with wrong password."""
    test_username = "wrongpassuser"
    test_password = "correctpassword"
    create_test_user(
        name="Wrong Pass User",
        username=test_username,
        email="wrongpass@example.com",
        password=test_password,
        role="staff",
        save=True
    )
    # db_session.commit()

    login_payload = {"username": test_username, "password": "wrongpassword"}
    res = testapp.post_json('/api/v1/auth/login', login_payload, status=401) # Harapannya 401 Unauthorized
    
    assert res.json['message'] == 'Invalid username or password.'

def test_login_failure_user_not_found(testapp):
    """Test login failure for a non-existent user."""
    login_payload = {"username": "nonexistentuser", "password": "anypassword"}
    res = testapp.post_json('/api/v1/auth/login', login_payload, status=401)
    
    assert res.json['message'] == 'Invalid username or password.'

# Tambahkan tes untuk /auth/register dan /auth/me dengan berbagai skenario
# (sukses, duplikat, tanpa token, token salah, dll.)