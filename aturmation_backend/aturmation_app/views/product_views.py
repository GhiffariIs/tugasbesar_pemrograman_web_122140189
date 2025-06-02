# aturmation_app/views/product_views.py
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPCreated, HTTPOk, HTTPNotFound, HTTPBadRequest, HTTPNoContent
)
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy import or_, and_, asc, desc # Untuk filter & sort
import math

from ..models.product import Product
# from ..models.category import Category # Tidak diperlukan lagi

PRODUCT_VIEW_PERMISSION = 'product:view'
PRODUCT_ADD_PERMISSION = 'product:add'
PRODUCT_EDIT_PERMISSION = 'product:edit'
PRODUCT_DELETE_PERMISSION = 'product:delete'

def _validate_product_data(request, data, is_update=False, product_id_to_ignore_for_sku=None):
    errors = {}
    name = data.get('name')
    sku = data.get('sku')
    price_str = data.get('price')
    stock_str = data.get('stock')
    # min_stock_str = data.get('min_stock') # Hapus jika min_stock dihapus dari model

    if not is_update or 'name' in data:
        if not name or not isinstance(name, str) or len(name.strip()) == 0: errors['name'] = 'Product name is required and must be a non-empty string.'
        elif len(name) > 255: errors['name'] = 'Product name cannot exceed 255 characters.'
    if not is_update or 'sku' in data:
        if not sku or not isinstance(sku, str) or len(sku.strip()) == 0: errors['sku'] = 'SKU is required and must be a non-empty string.'
        elif len(sku) > 100: errors['sku'] = 'SKU cannot exceed 100 characters.'
        else:
            query = request.dbsession.query(Product).filter(Product.sku == sku)
            if product_id_to_ignore_for_sku: query = query.filter(Product.id != product_id_to_ignore_for_sku)
            if query.first(): errors['sku'] = f"SKU '{sku}' already exists."
    if not is_update or 'price' in data:
        if price_str is None: errors['price'] = 'Price is required.'
        else:
            try:
                price_float = float(price_str)
                if price_float <= 0: errors['price'] = 'Price must be greater than 0.'
            except (ValueError, TypeError): errors['price'] = 'Price must be a valid number.'
    if not is_update or 'stock' in data:
        if stock_str is None: errors['stock'] = 'Stock is required.'
        else:
            try:
                stock_int = int(stock_str)
                if stock_int < 0: errors['stock'] = 'Stock cannot be negative.'
            except (ValueError, TypeError): errors['stock'] = 'Stock must be a valid integer.'
    # Hapus validasi min_stock jika fieldnya dihapus dari model
    # Hapus validasi category_id
    
    if errors:
        raise HTTPBadRequest(json_body={'message': "Validation failed.", 'errors': errors})
    
    validated_data = {}
    if name is not None: validated_data['name'] = name
    if sku is not None: validated_data['sku'] = sku
    if data.get('description') is not None : validated_data['description'] = data.get('description')
    if price_str is not None: validated_data['price'] = float(price_str)
    if stock_str is not None: validated_data['stock'] = int(stock_str)
    # Jika min_stock masih ada:
    # if min_stock_str is not None: validated_data['min_stock'] = int(min_stock_str) 
    return validated_data

@view_config(route_name='api_products_collection', request_method='POST', renderer='json', permission=PRODUCT_ADD_PERMISSION)
def create_product_view(request):
    try:
        json_data = request.json_body
        validated_data = _validate_product_data(request, json_data)
        
        new_product = Product(
            name=validated_data['name'], sku=validated_data['sku'],
            description=validated_data.get('description'),
            price=validated_data['price'], stock=validated_data['stock']
            # min_stock=validated_data.get('min_stock') # Jika min_stock masih ada
        )
        request.dbsession.add(new_product)
        request.dbsession.flush()
        return HTTPCreated(json_body={'message': 'Product created successfully.', 'product': new_product.as_dict()})
    except HTTPBadRequest as e: return e
    except IntegrityError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'message': 'Product creation failed (e.g. SKU already exists).'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] create_product_view: Unexpected error - {type(e).__name__}: {e}")
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})

@view_config(route_name='api_products_collection', request_method='GET', renderer='json', permission=PRODUCT_VIEW_PERMISSION)
def get_all_products_view(request):
    try:
        # Sederhanakan filtering dan sorting untuk awal
        search_term = request.params.get('searchTerm')
        query = request.dbsession.query(Product)
        if search_term:
            search_like = f"%{search_term}%"
            query = query.filter(or_(Product.name.ilike(search_like), Product.sku.ilike(search_like)))
        
        total_products = query.count()
        # Implementasi pagination dasar
        try:
            page = int(request.params.get('page', 1))
            rows_per_page = int(request.params.get('rowsPerPage', 10))
        except ValueError:
            page = 1; rows_per_page = 10
        if page < 1: page = 1
        if rows_per_page < 1: rows_per_page = 10
        offset = (page - 1) * rows_per_page
        products = query.order_by(Product.name).offset(offset).limit(rows_per_page).all()
        
        return HTTPOk(json_body={
            'products': [p.as_dict() for p in products],
            'totalProducts': total_products,
            'currentPage': page,
            'totalPages': math.ceil(total_products / rows_per_page) if total_products > 0 else 1
        })
    except Exception as e:
        print(f"[DEBUG] get_all_products_view: Unexpected error - {type(e).__name__}: {e}")
        return HTTPBadRequest(json_body={'message': f"Error fetching products: {e}"})

@view_config(route_name='api_product_detail', request_method='GET', renderer='json', permission=PRODUCT_VIEW_PERMISSION)
def get_product_view(request):
    try:
        product_id_str = request.matchdict.get('id')
        try: product_id = int(product_id_str)
        except (ValueError, TypeError): raise HTTPBadRequest(json_body={'message': 'Invalid product ID format.'})
        
        product = request.dbsession.query(Product).get(product_id)
        if not product: raise HTTPNotFound(json_body={'message': 'Product not found.'})
        return HTTPOk(json_body={'product': product.as_dict()})
    except (HTTPBadRequest, HTTPNotFound) as e: return e
    except Exception as e:
        print(f"[DEBUG] get_product_view: Unexpected error - {type(e).__name__}: {e}")
        return HTTPBadRequest(json_body={'message': f"Error fetching product: {e}"})

@view_config(route_name='api_product_detail', request_method='PUT', renderer='json', permission=PRODUCT_EDIT_PERMISSION)
def update_product_view(request):
    try:
        product_id_str = request.matchdict.get('id')
        try: product_id = int(product_id_str)
        except (ValueError, TypeError): raise HTTPBadRequest(json_body={'message': 'Invalid product ID format.'})

        product = request.dbsession.query(Product).get(product_id)
        if not product: raise HTTPNotFound(json_body={'message': 'Product not found.'})

        data_from_request = request.json_body
        validated_data = _validate_product_data(request, data_from_request, is_update=True, product_id_to_ignore_for_sku=product.id)

        updated_count = 0
        for key, value in validated_data.items():
            if hasattr(product, key):
                setattr(product, key, value)
                updated_count += 1
        
        if not updated_count:
            return HTTPOk(json_body={'message': 'No valid fields to update or no changes detected.', 'product': product.as_dict()})

        request.dbsession.flush()
        return HTTPOk(json_body={'message': 'Product updated successfully.', 'product': product.as_dict()})
    except (HTTPBadRequest, HTTPNotFound) as e: return e
    except IntegrityError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'message': 'Product update failed (e.g. SKU already exists).'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_product_view: Unexpected error - {type(e).__name__}: {e}")
        return HTTPBadRequest(json_body={'message': f"An unexpected error occurred: {e}"})

@view_config(route_name='api_product_detail', request_method='DELETE', permission=PRODUCT_DELETE_PERMISSION)
def delete_product_view(request):
    try:
        product_id_str = request.matchdict.get('id')
        try: product_id = int(product_id_str)
        except (ValueError, TypeError): raise HTTPBadRequest(json_body={'message': 'Invalid product ID format.'})

        product = request.dbsession.query(Product).get(product_id)
        if not product: raise HTTPNotFound(json_body={'message': 'Product not found.'})
        
        request.dbsession.delete(product)
        # request.dbsession.flush() # Opsional, pyramid_tm akan commit
        return HTTPOk(json_body={'message': 'Product deleted successfully.'})
    except (HTTPBadRequest, HTTPNotFound) as e: return e
    except Exception as e: # Termasuk DBAPIError jika ada FK constraint
        request.dbsession.rollback()
        print(f"[DEBUG] delete_product_view: Unexpected error - {type(e).__name__}: {e}")
        if "foreign key constraint" in str(e).lower():
             return HTTPBadRequest(json_body={'message': 'Cannot delete product: It is currently in use.'})
        return HTTPBadRequest(json_body={'message': f"Error deleting product: {e}"})