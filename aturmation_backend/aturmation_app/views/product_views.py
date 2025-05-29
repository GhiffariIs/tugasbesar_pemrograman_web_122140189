from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPCreated,
    HTTPOk,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPNoContent,
    HTTPForbidden 
)
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm import joinedload # Untuk eager loading kategori

from ..models.product import Product
from ..models.category import Category # Untuk validasi category_id

# --- Definisikan Nama Permission (string) ---
PRODUCT_VIEW_PERMISSION = 'product:view'
PRODUCT_ADD_PERMISSION = 'product:add'
PRODUCT_EDIT_PERMISSION = 'product:edit'
PRODUCT_DELETE_PERMISSION = 'product:delete'


def validate_product_data(request, data, is_update=False, product_id_to_ignore_for_sku=None):
    """Fungsi helper untuk validasi data produk."""
    name = data.get('name')
    sku = data.get('sku')
    price = data.get('price')
    stock = data.get('stock')
    min_stock = data.get('min_stock')
    category_id = data.get('category_id')
    
    errors = {}

    if not is_update or 'name' in data: # Validasi name jika field ada atau saat create
        if not name: errors['name'] = 'Product name is required.'
        elif len(name) > 255: errors['name'] = 'Product name cannot exceed 255 characters.'

    if not is_update or 'sku' in data:
        if not sku: errors['sku'] = 'SKU is required.'
        elif len(sku) > 100: errors['sku'] = 'SKU cannot exceed 100 characters.'
        else: # Cek keunikan SKU
            query = request.dbsession.query(Product).filter(Product.sku == sku)
            if product_id_to_ignore_for_sku: # Saat update, abaikan produk itu sendiri
                query = query.filter(Product.id != product_id_to_ignore_for_sku)
            if query.first():
                errors['sku'] = f"SKU '{sku}' already exists."
                
    if not is_update or 'price' in data:
        if price is None: errors['price'] = 'Price is required.'
        else:
            try:
                price_float = float(price)
                if price_float <= 0: errors['price'] = 'Price must be greater than 0.'
            except ValueError:
                errors['price'] = 'Price must be a valid number.'

    if not is_update or 'stock' in data:
        if stock is None: errors['stock'] = 'Stock is required.'
        else:
            try:
                stock_int = int(stock)
                if stock_int < 0: errors['stock'] = 'Stock cannot be negative.'
            except ValueError:
                errors['stock'] = 'Stock must be a valid integer.'

    if not is_update or 'min_stock' in data:
        if min_stock is None: errors['min_stock'] = 'Minimum stock is required.'
        else:
            try:
                min_stock_int = int(min_stock)
                if min_stock_int < 0: errors['min_stock'] = 'Minimum stock cannot be negative.'
            except ValueError:
                errors['min_stock'] = 'Minimum stock must be a valid integer.'

    if not is_update or 'category_id' in data:
        if category_id is None: errors['category_id'] = 'Category ID is required.'
        else:
            try:
                category_id_int = int(category_id)
                category = request.dbsession.query(Category).get(category_id_int)
                if not category:
                    errors['category_id'] = f"Category with ID {category_id_int} not found."
            except ValueError:
                errors['category_id'] = 'Category ID must be a valid integer.'
    
    if errors:
        raise HTTPBadRequest(json_body={'errors': errors})
    
    # Kembalikan data yang sudah divalidasi/dikonversi jika perlu
    # Untuk sekarang, kita hanya melempar error jika ada.
    # View akan mengambil data langsung dari `data` jika tidak ada error.

@view_config(
    route_name='api_products_collection',
    request_method='POST',
    renderer='json',
    permission=PRODUCT_ADD_PERMISSION
)
def create_product_view(request):
    try:
        data = request.json_body
        print(f"[DEBUG] create_product_view: Received data: {data}")

        # Validasi data
        validate_product_data(request, data) 
        
        name = data.get('name')
        sku = data.get('sku')
        description = data.get('description')
        price = float(data.get('price'))
        stock = int(data.get('stock'))
        min_stock = int(data.get('min_stock'))
        category_id = int(data.get('category_id'))

        new_product = Product(
            name=name,
            sku=sku,
            description=description,
            price=price,
            stock=stock,
            min_stock=min_stock,
            category_id=category_id
        )
        request.dbsession.add(new_product)
        request.dbsession.flush() # Dapat ID dan error DB awal

        print(f"[DEBUG] create_product_view: Product '{name}' created with ID {new_product.id}")
        
        # Load kategori untuk dimasukkan dalam respons
        # Ini akan melakukan query tambahan, tapi memastikan data kategori ada.
        # Atau, Anda bisa mengandalkan `as_dict` untuk memuatnya jika sesi masih aktif.
        # product_for_response = request.dbsession.query(Product).options(joinedload(Product.category)).get(new_product.id)

        return HTTPCreated(json_body={
            'message': 'Product created successfully.',
            'product': new_product.as_dict(include_category_details=True) # Gunakan method dari model
        })
    except HTTPBadRequest as e: # Error dari validate_product_data
        return e # Kembalikan langsung HTTPBadRequest yang sudah ada
    except IntegrityError as e: # Jika ada unique constraint lain yang terlewat validasi
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: IntegrityError - {e}")
        return HTTPBadRequest(json_body={'message': f"Product creation failed due to a data conflict (e.g., SKU might already exist if not caught by validation)."})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: DBAPIError - {e}")
        return Response("Database error during product creation.", status=500)
    except ValueError: # Jika parsing float/int gagal setelah validasi (seharusnya tidak terjadi jika validasi ketat)
        print("[DEBUG] create_product_view: ValueError (type conversion)")
        return HTTPBadRequest(json_body={'message': 'Invalid data type for price, stock, min_stock, or category_id.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)

@view_config(
    route_name='api_products_collection',
    request_method='GET',
    renderer='json',
    permission=PRODUCT_VIEW_PERMISSION
)
def get_all_products_view(request):
    try:
        print("[DEBUG] get_all_products_view: Fetching all products")
        
        # TODO (Enhancement Nanti): Implementasi filtering & pagination sesuai spek frontend
        # searchTerm = request.params.get('searchTerm')
        # categoryFilter = request.params.get('categoryFilter')
        # stockStatusFilter = request.params.get('stockStatusFilter')
        # page = int(request.params.get('page', 1))
        # rowsPerPage = int(request.params.get('rowsPerPage', 10)) # limit
        # offset = (page - 1) * rowsPerPage
        
        # Versi dasar: ambil semua, eager load kategori
        products_query = request.dbsession.query(Product).options(joinedload(Product.category)).order_by(Product.name)
        # total_products = products_query.count() # Untuk pagination nanti
        products = products_query.all()
        
        return {
            'products': [product.as_dict(include_category_details=True) for product in products],
            # 'totalProducts': total_products # Untuk pagination nanti
        }
    except Exception as e: # Tangkap semua error untuk sekarang
        print(f"[DEBUG] get_all_products_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        # Frontend mengharapkan { products: [], totalProducts: N }
        # Jadi jika error, kembalikan struktur yang mirip tapi kosong atau pesan error
        return Response(f"Error fetching products: {e}", status=500)


@view_config(
    route_name='api_product_detail',
    request_method='GET',
    renderer='json',
    permission=PRODUCT_VIEW_PERMISSION
)
def get_product_view(request):
    try:
        product_id = request.matchdict.get('id')
        print(f"[DEBUG] get_product_view: Fetching product with ID {product_id}")

        # Eager load kategori
        product = request.dbsession.query(Product).options(joinedload(Product.category)).get(product_id)
        
        if not product:
            print(f"[DEBUG] get_product_view: Product ID {product_id} not found")
            raise HTTPNotFound(json_body={'message': 'Product not found.'})
        
        return {'product': product.as_dict(include_category_details=True)}
    except Exception as e:
        print(f"[DEBUG] get_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"Error fetching product: {e}", status=500)


@view_config(
    route_name='api_product_detail',
    request_method='PUT',
    renderer='json',
    permission=PRODUCT_EDIT_PERMISSION
)
def update_product_view(request):
    try:
        product_id = request.matchdict.get('id')
        print(f"[DEBUG] update_product_view: Attempting to update product ID {product_id}")

        product = request.dbsession.query(Product).get(product_id)
        if not product:
            print(f"[DEBUG] update_product_view: Product ID {product_id} not found for update")
            raise HTTPNotFound(json_body={'message': 'Product not found.'})

        data = request.json_body
        print(f"[DEBUG] update_product_view: Received data for update: {data}")

        # Validasi data, abaikan produk saat ini untuk cek SKU unik
        validate_product_data(request, data, is_update=True, product_id_to_ignore_for_sku=product.id)

        updated = False
        if 'name' in data:
            product.name = data['name']
            updated = True
        if 'sku' in data:
            product.sku = data['sku']
            updated = True
        if 'description' in data:
            product.description = data.get('description')
            updated = True
        if 'price' in data:
            product.price = float(data['price'])
            updated = True
        if 'stock' in data:
            product.stock = int(data['stock'])
            updated = True
        if 'min_stock' in data:
            product.min_stock = int(data['min_stock'])
            updated = True
        if 'category_id' in data:
            product.category_id = int(data['category_id'])
            updated = True
        
        if not updated:
             return HTTPOk(json_body={
                'message': 'No changes detected for product.',
                'product': product.as_dict(include_category_details=True)
            })

        request.dbsession.flush()
        print(f"[DEBUG] update_product_view: Product ID {product_id} updated.")
        
        # Re-fetch dengan joinedload untuk memastikan kategori ter-update di respons
        # product_for_response = request.dbsession.query(Product).options(joinedload(Product.category)).get(product.id)
        
        return HTTPOk(json_body={
            'message': 'Product updated successfully.',
            # Gunakan objek product yang sudah di-update, as_dict akan handle category
            'product': product.as_dict(include_category_details=True) 
        })
    except HTTPBadRequest as e: # Dari validate_product_data
        return e
    except IntegrityError as e: # Jika ada unique constraint lain yang terlewat validasi
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: IntegrityError - {e}")
        return HTTPBadRequest(json_body={'message': f"Product update failed due to a data conflict (e.g., SKU)."})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: DBAPIError - {e}")
        return Response("Database error updating product.", status=500)
    except ValueError: # Jika parsing float/int gagal
        print("[DEBUG] update_product_view: ValueError (type conversion)")
        return HTTPBadRequest(json_body={'message': 'Invalid data type for price, stock, min_stock, or category_id.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)


@view_config(
    route_name='api_product_detail',
    request_method='DELETE',
    permission=PRODUCT_DELETE_PERMISSION
)
def delete_product_view(request): # renderer tidak perlu jika hanya return HTTPNoContent
    try:
        product_id = request.matchdict.get('id')
        print(f"[DEBUG] delete_product_view: Attempting to delete product ID {product_id}")

        product = request.dbsession.query(Product).get(product_id)
        if not product:
            print(f"[DEBUG] delete_product_view: Product ID {product_id} not found for deletion")
            raise HTTPNotFound(json_body={'message': 'Product not found.'})

        # PERHATIAN: Frontend mengharapkan pesan sukses, jadi kita tidak bisa hanya HTTPNoContent
        # jika pesan dibutuhkan. Namun, 204 adalah standar. Kita akan coba kembalikan pesan.
        # Atau, frontend harusnya menangani 204 sebagai sukses.

        # TODO: Pertimbangkan apa yang terjadi jika produk ini ada di transaksi.
        # Untuk sekarang, hapus langsung.
        request.dbsession.delete(product)
        print(f"[DEBUG] delete_product_view: Product ID {product_id} deleted from session.")
        
        # Return HTTPOk dengan pesan agar frontend bisa menampilkannya
        # Meskipun 204 lebih standar untuk DELETE tanpa konten.
        # Jika ingin tetap dengan 204, frontend yang menyesuaikan.
        return HTTPOk(json_body={'message': 'Product deleted successfully.'}) 
        # return HTTPNoContent() # Alternatif standar

    except DBAPIError as e: # Misalnya jika ada foreign key constraint violation dari tabel lain
        request.dbsession.rollback()
        print(f"[DEBUG] delete_product_view: DBAPIError - {e}")
        return HTTPBadRequest(json_body={'message': 'Error deleting product. It might be in use or a database error occurred.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] delete_product_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)