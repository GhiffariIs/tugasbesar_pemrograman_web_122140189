# aturmation_app/routes.py
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Rute Autentikasi
    config.add_route('api_register', '/api/v1/auth/register')
    config.add_route('api_auth_login', '/api/v1/auth/login')
    config.add_route('api_auth_me', '/api/v1/auth/me')

    # Rute untuk User Profile
    config.add_route('api_user_profile_update', '/api/v1/users/me/profile')

    # Rute untuk Products
    config.add_route('api_products_collection', '/api/v1/products')
    config.add_route('api_product_detail', '/api/v1/products/{id}')
    
    # Hapus rute untuk Categories, Transactions, Dashboard kompleks

    config.scan('.views')