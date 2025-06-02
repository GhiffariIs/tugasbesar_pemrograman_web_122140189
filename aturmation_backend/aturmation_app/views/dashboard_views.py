from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPBadRequest
from sqlalchemy.sql import func
from sqlalchemy import cast, Date, case
from datetime import datetime, timedelta, timezone

from ..models.product import Product
from ..models.category import Category
from ..models.transaction import Transaction, TransactionType
# Pastikan semua model yang dibutuhkan sudah diimpor

# --- Definisikan Nama Permission (string) ---
DASHBOARD_VIEW_PERMISSION = 'dashboard:view' # Satu permission umum untuk semua data dashboard

@view_config(
    route_name='api_dashboard_summary',
    request_method='GET',
    renderer='json',
    permission=DASHBOARD_VIEW_PERMISSION
)
def dashboard_summary_view(request):
    try:
        print("[DEBUG] dashboard_summary_view: Fetching dashboard summary data")
        dbsession = request.dbsession

        total_products = dbsession.query(func.count(Product.id)).scalar()
        total_categories = dbsession.query(func.count(Category.id)).scalar()
        
        # Produk dengan stok di bawah atau sama dengan min_stock
        # Perhatikan: Frontend spec menyebut < minStock, tapi umumnya <= minStock juga dianggap rendah
        # Sesuaikan logika filter ini jika perlu (misal Product.stock <= Product.min_stock)
        low_stock_products_count = dbsession.query(func.count(Product.id)).filter(Product.stock < Product.min_stock).scalar()

        # Transaksi dalam 24 jam terakhir (contoh)
        one_day_ago = datetime.now() - timedelta(days=1)
        recent_transactions_count = dbsession.query(func.count(Transaction.id)).filter(Transaction.timestamp >= one_day_ago).scalar()

        summary_data = {
            "totalProducts": total_products if total_products is not None else 0,
            "totalCategories": total_categories if total_categories is not None else 0,
            "lowStockProducts": low_stock_products_count if low_stock_products_count is not None else 0,
            "recentTransactionsCount": recent_transactions_count if recent_transactions_count is not None else 0
        }
        
        print(f"[DEBUG] dashboard_summary_view: Summary data: {summary_data}")
        return HTTPOk(json_body=summary_data)

    except Exception as e:
        print(f"[DEBUG] dashboard_summary_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        # Kembalikan struktur error yang konsisten jika memungkinkan
        return HTTPBadRequest(json_body={'message': f"Error fetching dashboard summary: {e}"})
    
@view_config(
    route_name='api_dashboard_low_stock_items', # Nama rute dari routes.py
    request_method='GET',
    renderer='json',
    permission=DASHBOARD_VIEW_PERMISSION # Menggunakan permission yang sama
)
def dashboard_low_stock_items_view(request):
    try:
        # Ambil parameter 'limit' dari query string, default ke 5 jika tidak ada
        try:
            limit = int(request.params.get('limit', 5))
            if limit <= 0: # Batasi agar limit selalu positif
                limit = 5 
        except ValueError:
            limit = 5 # Default jika konversi gagal

        print(f"[DEBUG] dashboard_low_stock_items_view: Fetching low stock items with limit {limit}")
        dbsession = request.dbsession

        low_stock_items = dbsession.query(
            Product.id,
            Product.name,
            Product.sku, # Frontend mungkin butuh SKU juga
            Product.stock, # Nama kolom di DB adalah 'stock'
            Product.min_stock
        ).filter(Product.stock < Product.min_stock).order_by(
            (Product.min_stock - Product.stock).desc() # Urutkan berdasarkan seberapa parah kurangnya
        ).limit(limit).all()

        # Ubah hasil query (yang berupa tuple/NamedTuple) menjadi list of dictionaries
        # Sesuai ekspektasi frontend: [ { id, name, currentStock, minStock }, ... ]
        # Perhatikan penamaan field 'currentStock' vs 'stock' di model.
        result_list = [
            {
                "id": item.id,
                "name": item.name,
                "sku": item.sku, 
                "currentStock": item.stock, # Frontend mengharapkan 'currentStock'
                "minStock": item.min_stock
            } for item in low_stock_items
        ]

        print(f"[DEBUG] dashboard_low_stock_items_view: Found {len(result_list)} low stock items.")
        return HTTPOk(json_body=result_list) # Langsung return list of dictionaries

    except Exception as e:
        print(f"[DEBUG] dashboard_low_stock_items_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"Error fetching low stock items: {e}"})

# Lanjutan di aturmation_backend/aturmation_app/views/dashboard_views.py

# ... (impor dan view-view dashboard yang sudah ada) ...

@view_config(
    route_name='api_dashboard_recent_products', # Nama rute dari routes.py
    request_method='GET',
    renderer='json',
    permission=DASHBOARD_VIEW_PERMISSION # Menggunakan permission yang sama
)
def dashboard_recent_products_view(request):
    try:
        # Ambil parameter 'limit' dari query string, default ke 5 jika tidak ada
        try:
            limit = int(request.params.get('limit', 5)) # Frontend spec menggunakan 'limit=N'
            if limit <= 0: 
                limit = 5 
        except ValueError:
            limit = 5 

        print(f"[DEBUG] dashboard_recent_products_view: Fetching recent products with limit {limit}")
        dbsession = request.dbsession

        # Mengambil produk terbaru berdasarkan 'created_at' (atau 'updated_at' jika lebih relevan)
        # Kita juga perlu nama kategori, jadi kita join dengan Category
        recent_products = dbsession.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.price,
            Product.created_at, # Untuk pengurutan dan mungkin info tambahan
            Category.name.label('category_name') # Ambil nama kategori dan beri label
        ).join(Product.category).order_by( # Lakukan join dari Product ke Category
            Product.created_at.desc() # Urutkan dari yang paling baru dibuat
        ).limit(limit).all()

        # Ubah hasil query (yang berupa tuple/NamedTuple) menjadi list of dictionaries
        # Sesuai ekspektasi frontend: [ { id, name, stock, categoryName, price }, ... ]
        result_list = [
            {
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "categoryName": product.category_name, # Gunakan label dari query
                "price": product.price,
                # "createdAt": product.created_at.isoformat() # Opsional jika frontend butuh
            } for product in recent_products
        ]

        print(f"[DEBUG] dashboard_recent_products_view: Found {len(result_list)} recent products.")
        return HTTPOk(json_body=result_list) # Langsung return list of dictionaries

    except Exception as e:
        print(f"[DEBUG] dashboard_recent_products_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"Error fetching recent products: {e}"})

@view_config(
    route_name='api_dashboard_transaction_chart', # Nama rute dari routes.py
    request_method='GET',
    renderer='json',
    permission=DASHBOARD_VIEW_PERMISSION # Menggunakan permission yang sama
)
def dashboard_transaction_chart_view(request):
    try:
        period = request.params.get('period', 'week') # Default ke 'week' jika tidak ada
        print(f"[DEBUG] dashboard_transaction_chart_view: Fetching data for period: {period}")
        dbsession = request.dbsession

        today = datetime.now(timezone.utc).date() # Gunakan timezone-aware datetime untuk now() lalu ambil date()

        if period == 'week':
            # Ambil data 7 hari terakhir termasuk hari ini
            start_date = today - timedelta(days=6)
            date_trunc_func = func.date_trunc('day', Transaction.timestamp)
            # Untuk label, kita bisa tampilkan tanggalnya saja atau nama hari
            # Jika ingin nama hari, frontend yang bisa format dari tanggal
        elif period == 'month':
            # Ambil data 30 hari terakhir termasuk hari ini
            start_date = today - timedelta(days=29)
            date_trunc_func = func.date_trunc('day', Transaction.timestamp)
        else:
            raise HTTPBadRequest(json_body={'message': "Invalid period. Use 'week' or 'month'."})

        # Query untuk mengambil total quantity stock_in dan stock_out per hari
        # dalam rentang tanggal yang ditentukan
        transactions_by_day = dbsession.query(
            cast(date_trunc_func, Date).label('transaction_date'), # Ambil tanggalnya saja
            func.sum(
                case(
                    (Transaction.type == TransactionType.stock_in, Transaction.quantity), # Jika stock_in, jumlahkan quantity
                    else_=0 # Selain itu, anggap 0 untuk sum stock_in
                )
            ).label('total_stock_in'),
            func.sum(
                case(
                    (Transaction.type == TransactionType.stock_out, Transaction.quantity),# Jika stock_out, jumlahkan quantity
                    else_=0 # Selain itu, anggap 0 untuk sum stock_out
                )
            ).label('total_stock_out')
        ).filter(
            cast(Transaction.timestamp, Date) >= start_date,
            cast(Transaction.timestamp, Date) <= today # Sampai akhir hari ini
        ).group_by(
            'transaction_date' # Group berdasarkan tanggal
        ).order_by(
            'transaction_date' # Urutkan berdasarkan tanggal
        ).all()

        # Siapkan data untuk respons frontend
        labels = []
        stock_in_data = []
        stock_out_data = []

        # Buat daftar semua tanggal dalam rentang untuk memastikan semua hari ada di label
        # meskipun tidak ada transaksi pada hari tersebut.
        current_date = start_date
        all_dates_in_period = {} # Dictionary untuk mapping tanggal ke data transaksi
        while current_date <= today:
            labels.append(current_date.strftime('%Y-%m-%d')) # Format tanggal YYYY-MM-DD
            all_dates_in_period[current_date] = {'stock_in': 0, 'stock_out': 0}
            current_date += timedelta(days=1)

        # Isi data transaksi ke dictionary all_dates_in_period
        for record in transactions_by_day:
            # record.transaction_date adalah objek date dari hasil query
            if record.transaction_date in all_dates_in_period:
                all_dates_in_period[record.transaction_date]['stock_in'] = record.total_stock_in or 0
                all_dates_in_period[record.transaction_date]['stock_out'] = record.total_stock_out or 0

        # Ambil data dari dictionary sesuai urutan label (semua tanggal dalam periode)
        for dt_str in labels:
            dt_obj = datetime.strptime(dt_str, '%Y-%m-%d').date() # Konversi string label kembali ke date object
            stock_in_data.append(all_dates_in_period[dt_obj]['stock_in'])
            stock_out_data.append(all_dates_in_period[dt_obj]['stock_out'])

        response_data = {
            "labels": labels, # List of date strings
            "stockInData": stock_in_data,
            "stockOutData": stock_out_data
        }

        print(f"[DEBUG] dashboard_transaction_chart_view: Chart data: {response_data}")
        return HTTPOk(json_body=response_data)

    except HTTPBadRequest as e:
        return e
    except Exception as e:
        print(f"[DEBUG] dashboard_transaction_chart_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"Error fetching transaction chart data: {e}"})

# View untuk endpoint dashboard lainnya akan ditambahkan di sini nanti
# GET /dashboard/low-stock-items?limit=N
# GET /dashboard/recent-products?limit=N
# GET /dashboard/transaction-chart?period={week|month}