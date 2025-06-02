# aturmation_app/routes.py
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Rute Autentikasi
    config.add_route('api_register', '/api/v1/auth/register')
    config.add_route('api_auth_login', '/api/v1/auth/login')
    config.add_route('api_auth_me', '/api/v1/auth/me')

    # Rute untuk Categories
    config.add_route('api_categories_collection', '/api/v1/categories')
    config.add_route('api_category_detail', '/api/v1/categories/{id}')

    # Rute untuk Products
    config.add_route('api_products_collection', '/api/v1/products')
    config.add_route('api_product_detail', '/api/v1/products/{id}')

    config.add_route('api_transactions_collection', '/api/v1/transactions')

    # === Rute untuk Dashboard ===
    config.add_route('api_dashboard_summary', '/api/v1/dashboard/summary')
    config.add_route('api_dashboard_low_stock_items', '/api/v1/dashboard/low-stock-items')
    config.add_route('api_dashboard_recent_products', '/api/v1/dashboard/recent-products')
    config.add_route('api_dashboard_transaction_chart', '/api/v1/dashboard/transaction-chart')

    # Rute untuk User Profile
    config.add_route('api_user_profile_update', '/api/v1/users/me/profile')

    config.scan('.views')