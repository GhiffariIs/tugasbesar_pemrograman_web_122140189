def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600) # Jika ada file statis

    # Rute untuk Autentikasi
    config.add_route('api_register', '/api/v1/auth/register')
    config.add_route('api_auth_login', '/api/v1/auth/login')
    config.add_route('api_auth_me', '/api/v1/auth/me')

    # Rute untuk items kategori
    config.add_route('api_categories_collection', '/api/v1/categories')
    config.add_route('api_category_detail', '/api/v1/categories/{id}')

    # Rute untuk CRUD Items
    config.add_route('api_items_collection', '/api/v1/items')
    config.add_route('api_item_detail', '/api/v1/items/{id}')

    config.scan('.views') # Memastikan view di-scan