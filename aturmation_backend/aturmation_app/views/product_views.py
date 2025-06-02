# aturmation_backend/aturmation_app/views/product_views.py

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPCreated,
    HTTPOk,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPNoContent, # Bisa digunakan untuk DELETE jika frontend menangani 204
    HTTPForbidden # Untuk error otorisasi jika perlu
)
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_, asc, desc
import math

from ..models.product import Product
from ..models.category import Category

# --- Definisi Nama Permission (Konsisten dengan security.py) ---
PRODUCT_VIEW_PERMISSION = 'product:view'
PRODUCT_ADD_PERMISSION = 'product:add'
PRODUCT_EDIT_PERMISSION = 'product:edit'
PRODUCT_DELETE_PERMISSION = 'product:delete'


def _validate_product_data(request, data, is_update=False, product_id_to_ignore_for_sku=None):
    """Fungsi helper internal untuk validasi data produk."""
    errors = {}
    
    # Ambil data dengan aman
    name = data.get('name')
    sku = data.get('sku')
    price_str = data.get('price')
    stock_str = data.get('stock')
    min_stock_str = data.get('min_stock')
    category_id_str = data.get('category_id')
    # description opsional, jadi tidak perlu validasi khusus 'required'

    # Validasi Name
    if not is_update or 'name' in data:
        if not name: errors['name'] = 'Product name is required.'
        elif not isinstance(name, str) or len(name.strip()) == 0 : errors['name'] = 'Product name must be a non-empty string.'
        elif len(name) > 255: errors['name'] = 'Product name cannot exceed 255 characters.'

    # Validasi SKU
    if not is_update or 'sku' in data:
        if not sku: errors['sku'] = 'SKU is required.'
        elif not isinstance(sku, str) or len(sku.strip()) == 0: errors['sku'] = 'SKU must be a non-empty string.'
        elif len(sku) > 100: errors['sku'] = 'SKU cannot exceed 100 characters.'
        else:
            query = request.dbsession.query(Product).filter(Product.sku == sku)
            if product_id_to_ignore_for_sku:
                query = query.filter(Product.id != product_id_to_ignore_for_sku)
            if query.first():
                errors['sku'] = f"SKU '{sku}' already exists."
                
    # Validasi Price
    if not is_update or 'price' in data:
        if price_str is None: errors['price'] = 'Price is required.'
        else:
            try:
                price_float = float(price_str)
                if price_float <= 0: errors['price'] = 'Price must be greater than 0.'
            except (ValueError, TypeError):
                errors['price'] = 'Price must be a valid number.'

    # Validasi Stock
    if not is_update or 'stock' in data:
        if stock_str is None: errors['stock'] = 'Stock is required.'
        else:
            try:
                stock_int = int(stock_str)
                if stock_int < 0: errors['stock'] = 'Stock cannot be negative.'
            except (ValueError, TypeError):
                errors['stock'] = 'Stock must be a valid integer.'

    # Validasi Minimum Stock
    if not is_update or 'min_stock' in data:
        if min_stock_str is None: errors['min_stock'] = 'Minimum stock is required.'
        else:
            try:
                min_stock_int = int(min_stock_str)
                if min_stock_int < 0: errors['min_stock'] = 'Minimum stock cannot be negative.'
            except (ValueError, TypeError):
                errors['min_stock'] = 'Minimum stock must be a valid integer.'

    # Validasi Category ID
    if not is_update or 'category_id' in data:
        if category_id_str is None: errors['category_id'] = 'Category ID is required.'
        else:
            try:
                category_id_int = int(category_id_str)
                category = request.dbsession.query(Category).get(category_id_int)
                if not category:
                    errors['category_id'] = f"Category with ID {category_id_int} not found."
            except (ValueError, TypeError):
                errors['category_id'] = 'Category ID must be a valid integer.'
    
    if errors:
        error_message = "Validation failed. Please check the details."
        # Anda bisa membuat pesan yang lebih detail jika mau:
        # error_details = "; ".join([f"{k}: {v}" for k, v in errors.items()])
        # error_message = f"Validation failed: {error_details}"
        raise HTTPBadRequest(json_body={'message': error_message, 'errors': errors})
    
    # Mengembalikan data yang sudah dikoversi dan siap pakai jika validasi lolos
    # Ini opsional, view bisa melakukan konversi sendiri, tapi ini bisa merapikan view.
    validated_data = {}
    if name is not None: validated_data['name'] = name
    if sku is not None: validated_data['sku'] = sku
    if data.get('description') is not None : validated_data['description'] = data.get('description') # Deskripsi boleh null
    if price_str is not None: validated_data['price'] = float(price_str)
    if stock_str is not None: validated_data['stock'] = int(stock_str)
    if min_stock_str is not None: validated_data['min_stock'] = int(min_stock_str)
    if category_id_str is not None: validated_data['category_id'] = int(category_id_str)
    
    return validated_data


@view_config(
    route_name='api_products_collection',
    request_method='POST',
    renderer='json',
    permission=PRODUCT_ADD_PERMISSION
)
def create_product_view(request):
    try:
        json_data_from_request = request.json_body
        print(f"[DEBUG] create_product_view: Received data: {json_data_from_request}")

        # Validasi data dan dapatkan data yang sudah dikonversi jika valid
        validated_data = _validate_product_data(request, json_data_from_request)
        
        new_product = Product(
            name=validated_data['name'],
            sku=validated_data['sku'],
            description=validated_data.get('description'), # .get() karena deskripsi opsional
            price=validated_data['price'],
            stock=validated_data['stock'],
            min_stock=validated_data['min_stock'],
            category_id=validated_data['category_id']
        )
        request.dbsession.add(new_product)
        request.dbsession.flush() 

        print(f"[DEBUG] create_product_view: Product '{validated_data['name']}' created with ID {new_product.id}")
        
        # Eager load kategori untuk respons yang lengkap
        product_for_response = request.dbsession.query(Product).options(joinedload(Product.category)).get(new_product.id)

        return HTTPCreated(json_body={
            'message': 'Product created successfully.',
            'product': product_for_response.as_dict(include_category_details=True)
        })
    except HTTPBadRequest as e: # Error dari _validate_product_data
        return e 
    except IntegrityError as e: 
        request.dbsession.rollback()
        sku_sent = json_data_from_request.get('sku', 'unknown')
        print(f"[DEBUG] create_product_view: IntegrityError - {e}")
        if 'uq_products_sku' in str(e).lower() or ('unique constraint' in str(e).lower() and 'sku' in str(e).lower()):
             return HTTPBadRequest(json_body={'message': 'Product creation failed.', 'errors': {'sku': f"SKU '{sku_sent}' already exists."}})
        return HTTPBadRequest(json_body={'message': 'Product creation failed due to a data conflict.'})
    except DBAPIError as e: # Error database umum
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: DBAPIError - {e}")
        return HTTPBadRequest(json_body={'message': "Database error during product creation."})
    except Exception as e: # Tangkap error tak terduga lainnya
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})


@view_config(
    route_name='api_products_collection',
    request_method='GET',
    renderer='json',
    permission=PRODUCT_VIEW_PERMISSION # Asumsi permission PRODUCT_VIEW_PERMISSION sudah ada
)
def get_all_products_view(request):
    try:
        print("[DEBUG] get_all_products_view: Fetching all products with filters/pagination/sorting")
        dbsession = request.dbsession

        # --- Ambil Parameter Query ---
        # Pagination
        try:
            page = int(request.params.get('page', 1))
            rows_per_page = int(request.params.get('rowsPerPage', 10))
            if page < 1: page = 1
            if rows_per_page < 1: rows_per_page = 10
            if rows_per_page > 100: rows_per_page = 100
        except ValueError:
            page = 1
            rows_per_page = 10
        offset = (page - 1) * rows_per_page

        # Filtering
        search_term = request.params.get('searchTerm')
        category_filter_str = request.params.get('categoryFilter')
        stock_status_filter = request.params.get('stockStatusFilter')

        # === BARU: Sorting Parameters ===
        sort_by = request.params.get('sort_by', 'name') # Default sort berdasarkan nama
        sort_order_str = request.params.get('sort_order', 'asc').lower() # Default ascending

        if sort_order_str not in ['asc', 'desc']:
            sort_order_str = 'asc' # Default ke asc jika tidak valid

        sort_order_func = asc if sort_order_str == 'asc' else desc
        # ===============================

        # --- Bangun Query Dasar ---
        query = dbsession.query(Product).options(joinedload(Product.category))

        # --- Terapkan Filter (kode filter yang sudah ada) ---
        if search_term:
            search_like = f"%{search_term}%"
            query = query.filter(or_(Product.name.ilike(search_like), Product.sku.ilike(search_like)))
            print(f"[DEBUG] Applied searchTerm filter: {search_term}")

        if category_filter_str:
            try:
                category_id = int(category_filter_str)
                query = query.filter(Product.category_id == category_id)
                print(f"[DEBUG] Applied categoryFilter: {category_id}")
            except ValueError:
                print(f"[DEBUG] Invalid categoryFilter (not an int): {category_filter_str}")
                pass 

        if stock_status_filter and stock_status_filter != 'all':
            if stock_status_filter == 'inStock':
                query = query.filter(Product.stock > Product.min_stock)
            elif stock_status_filter == 'lowStock':
                query = query.filter(and_(Product.stock <= Product.min_stock, Product.stock > 0))
            elif stock_status_filter == 'outOfStock':
                query = query.filter(Product.stock == 0)
            print(f"[DEBUG] Applied stockStatusFilter: {stock_status_filter}")

        # --- Dapatkan Total Item Setelah Filter ---
        total_products = query.count()
        print(f"[DEBUG] Total products after filtering: {total_products}")

        # === BARU: Terapkan Sorting ===
        # Definisikan kolom yang diizinkan untuk di-sort dan mapping ke atribut model
        allowed_sort_fields = {
            'name': Product.name,
            'price': Product.price,
            'stock': Product.stock,
            'created_at': Product.created_at,
            'updated_at': Product.updated_at,
            'sku': Product.sku
            # Tambahkan field lain jika perlu, misal category_name (membutuhkan join atau alias)
        }

        sort_column = allowed_sort_fields.get(sort_by)
        if sort_column is None:
            sort_column = Product.name # Default jika sort_by tidak valid
            print(f"[DEBUG] Invalid sort_by value '{sort_by}', defaulting to 'name'")

        query = query.order_by(sort_order_func(sort_column))
        print(f"[DEBUG] Applied sorting: by '{sort_by}' order '{sort_order_str}'")
        # ============================

        # --- Terapkan Pagination ke Query ---
        products = query.offset(offset).limit(rows_per_page).all()

        total_pages = math.ceil(total_products / rows_per_page) if total_products > 0 else 1

        response_data = {
            'products': [product.as_dict(include_category_details=True) for product in products],
            'totalProducts': total_products,
            'currentPage': page,
            'totalPages': total_pages,
            'rowsPerPage': rows_per_page,
            'sortBy': sort_by, # Kembalikan parameter sort yang digunakan
            'sortOrder': sort_order_str # Kembalikan parameter order yang digunakan
        }

        print(f"[DEBUG] get_all_products_view: Returning {len(products)} products. Page: {page}, TotalPages: {total_pages}, Sort: {sort_by} {sort_order_str}")
        return HTTPOk(json_body=response_data)

    except Exception as e: 
        print(f"[DEBUG] get_all_products_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"Error fetching products: {e}", 'products': [], 'totalProducts': 0})


@view_config(
    route_name='api_product_detail',
    request_method='PUT',
    renderer='json',
    permission=PRODUCT_EDIT_PERMISSION
)
def update_product_view(request):
    try:
        product_id_str = request.matchdict.get('id')
        print(f"[DEBUG] update_product_view: Attempting to update product ID '{product_id_str}'")

        if product_id_str is None:
            raise HTTPNotFound(json_body={'message': 'Product ID missing in URL.'})
        try:
            product_id = int(product_id_str)
        except ValueError:
            raise HTTPBadRequest(json_body={'message': f"Invalid product ID format: '{product_id_str}'. ID must be an integer."})

        product = request.dbsession.query(Product).get(product_id)
        if not product:
            print(f"[DEBUG] update_product_view: Product ID {product_id} not found for update")
            raise HTTPNotFound(json_body={'message': 'Product not found.'})

        data_from_request = request.json_body
        print(f"[DEBUG] update_product_view: Received data for update: {data_from_request}")

        # Validasi hanya field yang dikirim, abaikan produk saat ini untuk cek SKU unik
        validated_data = _validate_product_data(request, data_from_request, is_update=True, product_id_to_ignore_for_sku=product.id)

        updated_fields_count = 0
        # Gunakan validated_data untuk update karena sudah dikonversi tipenya jika ada
        if 'name' in validated_data: # Cek di validated_data jika ada proses konversi/pembersihan
            product.name = validated_data['name']
            updated_fields_count +=1
        if 'sku' in validated_data:
            product.sku = validated_data['sku']
            updated_fields_count +=1
        if 'description' in data_from_request: # Deskripsi boleh null, jadi cek di data asli
            product.description = data_from_request.get('description')
            updated_fields_count +=1
        if 'price' in validated_data:
            product.price = validated_data['price']
            updated_fields_count +=1
        if 'stock' in validated_data:
            product.stock = validated_data['stock']
            updated_fields_count +=1
        if 'min_stock' in validated_data:
            product.min_stock = validated_data['min_stock']
            updated_fields_count +=1
        if 'category_id' in validated_data:
            product.category_id = validated_data['category_id']
            updated_fields_count +=1
        
        if updated_fields_count == 0: # Jika tidak ada field valid yang diupdate
             return HTTPOk(json_body={
                'message': 'No valid fields provided for update or no changes detected.',
                'product': product.as_dict(include_category_details=True)
            })

        request.dbsession.flush()
        print(f"[DEBUG] update_product_view: Product ID {product_id} updated.")
        
        product_for_response = request.dbsession.query(Product).options(joinedload(Product.category)).get(product.id)
        
        return HTTPOk(json_body={
            'message': 'Product updated successfully.',
            'product': product_for_response.as_dict(include_category_details=True) 
        })
    except (HTTPBadRequest, HTTPNotFound) as e: 
        return e
    except IntegrityError as e: 
        request.dbsession.rollback()
        sku_sent = data_from_request.get('sku', 'unknown') # Ambil dari data asli request
        print(f"[DEBUG] update_product_view: IntegrityError - {e}")
        if 'uq_products_sku' in str(e).lower() or ('unique constraint' in str(e).lower() and 'sku' in str(e).lower()):
             return HTTPBadRequest(json_body={'message': 'Product update failed.', 'errors': {'sku': f"SKU '{sku_sent}' already exists for another product."}})
        return HTTPBadRequest(json_body={'message': 'Product update failed due to a data conflict.'})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: DBAPIError - {e}")
        return HTTPBadRequest(json_body={'message': "Database error updating product."})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})


@view_config(
    route_name='api_product_detail',
    request_method='DELETE',
    permission=PRODUCT_DELETE_PERMISSION 
    # renderer='json' tidak wajib jika hanya return HTTPNoContent atau HTTPOk dengan body eksplisit
)
def delete_product_view(request):
    try:
        product_id_str = request.matchdict.get('id')
        print(f"[DEBUG] delete_product_view: Attempting to delete product ID '{product_id_str}'")

        if product_id_str is None:
            raise HTTPNotFound(json_body={'message': 'Product ID missing in URL.'})
        try:
            product_id = int(product_id_str)
        except ValueError:
            raise HTTPBadRequest(json_body={'message': f"Invalid product ID format: '{product_id_str}'. ID must be an integer."})

        product = request.dbsession.query(Product).get(product_id)
        if not product:
            print(f"[DEBUG] delete_product_view: Product ID {product_id} not found for deletion")
            raise HTTPNotFound(json_body={'message': 'Product not found.'})

        # TODO: Pertimbangkan apa yang terjadi jika produk ini ada di transaksi.
        # (Misal, cek relasi atau gunakan try-except untuk IntegrityError dari DB jika ada FK constraint)

        request.dbsession.delete(product)
        print(f"[DEBUG] delete_product_view: Product ID {product_id} deleted from session.")
        
        # Frontend Anda mengharapkan pesan sukses (dari analisis awal)
        return HTTPOk(json_body={'message': 'Product deleted successfully.'}) 
        # Alternatif standar: return HTTPNoContent() 

    except (HTTPBadRequest, HTTPNotFound) as e:
        return e
    except DBAPIError as e: 
        request.dbsession.rollback()
        print(f"[DEBUG] delete_product_view: DBAPIError - {e}")
        # Cek apakah error karena foreign key (produk digunakan di transaksi, dll.)
        if "foreign key constraint" in str(e).lower():
            return HTTPBadRequest(json_body={'message': 'Cannot delete product: It is currently in use (e.g., in transactions).'})
        return HTTPBadRequest(json_body={'message': 'Error deleting product due to a database issue.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] delete_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})