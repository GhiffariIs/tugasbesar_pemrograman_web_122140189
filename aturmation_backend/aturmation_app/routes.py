def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600) # Jika ada file statis

    # Rute untuk CRUD Items
    config.add_route('api_items_collection', '/api/v1/items')
    config.add_route('api_item_detail', '/api/v1/items/{id}')

    # Rute untuk Autentikasi
    config.add_route('api_register', '/api/v1/auth/register')
    # config.add_route('api_login_check', '/api/v1/auth/login_check') # Jika perlu endpoint login_check

    config.scan('.views') # Memastikan view di-scan