from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPCreated,
    HTTPOk,
    HTTPBadRequest,
    HTTPForbidden # Jika diperlukan untuk pengecekan manual
)
from sqlalchemy.exc import IntegrityError, DBAPIError, OperationalError
from sqlalchemy.orm import joinedload

from ..models.transaction import Transaction, TransactionType
from ..models.product import Product
from ..models.user import User # Untuk mengambil user_id

# --- Definisikan Nama Permission (string) ---
TRANSACTION_ADD_PERMISSION = 'transaction:add'
TRANSACTION_VIEW_PERMISSION = 'transaction:view'

@view_config(
    route_name='api_transactions_collection',
    request_method='POST',
    renderer='json',
    permission=TRANSACTION_ADD_PERMISSION
)
def create_transaction_view(request):
    try:
        data = request.json_body
        print(f"[DEBUG] create_transaction_view: Received data: {data}")

        product_id_str = data.get('product_id')
        transaction_type_str = data.get('type')
        quantity_str = data.get('quantity')
        notes = data.get('notes') # Opsional
        user_id = request.authenticated_userid # Diambil dari token JWT

        # --- Validasi Input ---
        errors = {}
        if not product_id_str: errors['product_id'] = "Product ID is required."
        if not transaction_type_str: errors['type'] = "Transaction type is required."
        if not quantity_str: errors['quantity'] = "Quantity is required."
        if not user_id: # Seharusnya tidak terjadi jika permission di-set
            print("[DEBUG] create_transaction_view: User ID not found from token (should be protected by permission).")
            return HTTPForbidden(json_body={'message': 'Authentication required.'})

        product_id, quantity = None, None

        if not errors: # Lanjutkan validasi jika field dasar ada
            try:
                product_id = int(product_id_str)
            except (ValueError, TypeError):
                errors['product_id'] = "Product ID must be a valid integer."
            
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    errors['quantity'] = "Quantity must be a positive integer."
            except (ValueError, TypeError):
                errors['quantity'] = "Quantity must be a valid integer."

            try:
                # Konversi string tipe transaksi ke Enum TransactionType
                transaction_type_enum = TransactionType[transaction_type_str]
            except KeyError:
                valid_types = [t.value for t in TransactionType]
                errors['type'] = f"Invalid transaction type. Valid types are: {', '.join(valid_types)}."
            
            # Cek apakah produk ada
            if product_id and not errors.get('product_id'):
                product = request.dbsession.query(Product).get(product_id)
                if not product:
                    errors['product_id'] = f"Product with ID {product_id} not found."
            else:
                product = None # Untuk menghindari error jika product_id tidak valid

        if errors:
            print(f"[DEBUG] create_transaction_view: Validation errors: {errors}")
            raise HTTPBadRequest(json_body={'message': "Validation failed.", 'errors': errors})

        # --- Logika Update Stok dan Buat Transaksi (dalam satu transaksi DB) ---
        # pyramid_tm akan menangani commit/rollback di level request
        
        print(f"[DEBUG] create_transaction_view: Processing transaction type '{transaction_type_enum.value}' for product ID {product.id} with quantity {quantity}")

        if transaction_type_enum == TransactionType.stock_in or \
           transaction_type_enum == TransactionType.initial_stock:
            product.stock += quantity
            print(f"[DEBUG] create_transaction_view: Stock IN/INITIAL. Product ID {product.id} stock updated to {product.stock}")
        
        elif transaction_type_enum == TransactionType.stock_out:
            if product.stock < quantity:
                print(f"[DEBUG] create_transaction_view: Insufficient stock for product ID {product.id}. Current: {product.stock}, Requested: {quantity}")
                raise HTTPBadRequest(json_body={
                    'message': 'Transaction failed.', 
                    'errors': {'quantity': f"Insufficient stock for product '{product.name}'. Available: {product.stock}, Requested: {quantity}."}
                })
            product.stock -= quantity
            print(f"[DEBUG] create_transaction_view: Stock OUT. Product ID {product.id} stock updated to {product.stock}")

        elif transaction_type_enum == TransactionType.adjustment:
            # Untuk adjustment, quantity yang dikirim adalah stok baru
            product.stock = quantity 
            print(f"[DEBUG] create_transaction_view: Stock ADJUSTMENT. Product ID {product.id} stock set to {product.stock}")
        
        # Simpan perubahan stok produk (pyramid_tm akan commit)
        # request.dbsession.add(product) # Tidak perlu jika sudah di-track sesi

        # Buat record transaksi baru
        new_transaction = Transaction(
            product_id=product.id,
            user_id=user_id,
            type=transaction_type_enum,
            quantity=quantity,
            notes=notes
        )
        request.dbsession.add(new_transaction)
        request.dbsession.flush() # Dapat ID transaksi dan error DB awal

        print(f"[DEBUG] create_transaction_view: Transaction record created with ID {new_transaction.id}")

        return HTTPCreated(json_body={
            'message': 'Transaction created successfully.',
            'transaction': new_transaction.as_dict(include_product_details=True, include_user_details=True),
            'updated_product_stock': product.stock # Kembalikan stok produk terbaru
        })

    except HTTPBadRequest as e:
        # request.dbsession.rollback() # pyramid_tm akan rollback jika ada exception
        return e
    except (IntegrityError, DBAPIError, OperationalError) as e: # Termasuk OperationalError untuk masalah koneksi/DB lain
        request.dbsession.rollback()
        print(f"[DEBUG] create_transaction_view: Database Error - {type(e).__name__}: {e}")
        return HTTPBadRequest(json_body={'message': "Database error during transaction processing."})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] create_transaction_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})


@view_config(
    route_name='api_transactions_collection',
    request_method='GET',
    renderer='json',
    permission=TRANSACTION_VIEW_PERMISSION
)
def get_all_transactions_view(request):
    try:
        print("[DEBUG] get_all_transactions_view: Fetching all transactions")
        
        # TODO (Enhancement Nanti): Implementasi filtering (product_id, type, date range) & pagination
        
        transactions_query = request.dbsession.query(Transaction).options(
            joinedload(Transaction.product).joinedload(Product.category), # Load product dan nested category-nya
            joinedload(Transaction.user) # Load user yang melakukan transaksi
        ).order_by(Transaction.timestamp.desc()) # Urutkan dari yang terbaru
        
        transactions = transactions_query.all()
        
        return {
            'transactions': [
                t.as_dict(include_product_details=True, include_user_details=True) 
                for t in transactions
            ]
            # 'totalTransactions': len(transactions) # Untuk pagination nanti
        }
    except Exception as e:
        print(f"[DEBUG] get_all_transactions_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"Error fetching transactions: {e}"})