"""Routes configuration"""

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # API Routes - all API routes will be prefixed with /api
    config.add_route('api_home', '/api')
    
    # Auth routes
    config.add_route('login', '/api/auth/login')
    config.add_route('register', '/api/auth/register')
    config.add_route('me', '/api/auth/me')
    
    # Category routes
    config.add_route('categories', '/api/categories')
    config.add_route('category', '/api/categories/{id}')
    
    # Product routes
    config.add_route('products', '/api/products')
    config.add_route('product', '/api/products/{id}')
    config.add_route('product_search', '/api/products/search')
    config.add_route('low_stock_products', '/api/products/low-stock')
    
    # Transaction routes
    config.add_route('transactions', '/api/transactions')
    config.add_route('transaction', '/api/transactions/{id}')
    config.add_route('stock_in_transactions', '/api/transactions/stock-in')
    config.add_route('stock_out_transactions', '/api/transactions/stock-out')
    
    # Report routes
    config.add_route('stock_report', '/api/reports/stock')
    config.add_route('transaction_report', '/api/reports/transactions')
    config.add_route('product_movement_report', '/api/reports/product-movement/{id}')
