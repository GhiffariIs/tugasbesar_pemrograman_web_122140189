# aturmation_app/views/product_views.py
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPInternalServerError
import sqlalchemy.exc
from sqlalchemy import desc, or_
import math
import logging

from ..models import Product

log = logging.getLogger(__name__)

# Simplified permissions
VIEW_PERMISSION = 'view'
CREATE_PERMISSION = 'create'
EDIT_PERMISSION = 'edit'
DELETE_PERMISSION = 'delete'

@view_config(route_name='api_products_collection', request_method='GET', renderer='json')
def get_products(request):
    """Get all products with pagination"""
    try:
        try:
            page = int(request.params.get('page', 1))
            per_page = int(request.params.get('per_page', 10))
            search = request.params.get('search', '')
        except (ValueError, TypeError):
            page = 1
            per_page = 10
            search = ''
        
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        
        query = request.dbsession.query(Product)
        
        # Apply search filter if provided
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.sku.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        # Apply ordering
        query = query.order_by(desc(Product.created_at))
        
        # Count total items
        total_items = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        products = query.limit(per_page).offset(offset).all()
        
        total_pages = math.ceil(total_items / per_page) if total_items > 0 else 0
        
        # Convert products to dict safely
        product_list = []
        for product in products:
            try:
                product_list.append(product.to_dict())
            except Exception as e:
                log.error(f"Error converting product to dict: {e}")
                # Skip this product if there's an error
                continue
        
        return {
            'status': 'success',
            'products': product_list,
            'pagination': {
                'total_items': total_items,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages
            }
        }
    except Exception as e:
        log.error(f"Error in get_products: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred while fetching products'
        })

@view_config(route_name='api_product_detail', request_method='GET', renderer='json')
def get_product(request):
    """Get a single product by ID"""
    try:
        product_id = request.matchdict['id']
        product = request.dbsession.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return HTTPNotFound(json_body={
                'status': 'error',
                'message': 'Product not found'
            })
        
        return {
            'status': 'success',
            'product': product.to_dict()
        }
    except Exception as e:
        log.error(f"Error in get_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred while fetching product'
        })

@view_config(route_name='api_products_collection', request_method='POST', permission=CREATE_PERMISSION, renderer='json')
def create_product(request):
    """Create a new product"""
    try:
        try:
            data = request.json_body
        except ValueError:
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Invalid JSON'
            })
        
        name = data.get('name')
        sku = data.get('sku')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock', 0)
        
        # Basic validation
        errors = {}
        if not name:
            errors['name'] = 'Name is required'
        if not sku:
            errors['sku'] = 'SKU is required'
        if not price:
            errors['price'] = 'Price is required'
        
        if errors:
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            })
        
        # Create a new product
        product = Product(
            name=name,
            sku=sku,
            description=description,
            price=float(price),  # Ensure price is float
            stock=int(stock) if stock else 0  # Ensure stock is integer
        )
        
        request.dbsession.add(product)
        request.dbsession.flush()
        
        return {
            'status': 'success',
            'message': 'Product created successfully',
            'product': product.to_dict()
        }
    except sqlalchemy.exc.IntegrityError as e:
        request.dbsession.rollback()
        
        # Check if error is due to duplicate SKU
        if 'unique constraint' in str(e).lower() and 'sku' in str(e).lower():
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A product with this SKU already exists'
            })
        
        log.error(f"Database error in create_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Database error occurred'
        })
    except Exception as e:
        request.dbsession.rollback()
        log.error(f"Error in create_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred while creating product'
        })

@view_config(route_name='api_product_detail', request_method='PUT', permission=EDIT_PERMISSION, renderer='json')
def update_product(request):
    """Update a product"""
    try:
        product_id = request.matchdict['id']
        product = request.dbsession.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return HTTPNotFound(json_body={
                'status': 'error',
                'message': 'Product not found'
            })
        
        try:
            data = request.json_body
        except ValueError:
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'Invalid JSON'
            })
        
        # Update fields if provided
        if 'name' in data and data['name']:
            product.name = data['name']
        if 'sku' in data and data['sku']:
            product.sku = data['sku']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])  # Ensure price is float
        if 'stock' in data:
            product.stock = int(data['stock'])  # Ensure stock is integer
        
        request.dbsession.flush()
        
        return {
            'status': 'success',
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }
    except sqlalchemy.exc.IntegrityError as e:
        request.dbsession.rollback()
        
        # Check if error is due to duplicate SKU
        if 'unique constraint' in str(e).lower() and 'sku' in str(e).lower():
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A product with this SKU already exists'
            })
        
        log.error(f"Database error in update_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Database error occurred'
        })
    except Exception as e:
        request.dbsession.rollback()
        log.error(f"Error in update_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': f'Server error occurred while updating product'
        })

@view_config(route_name='api_product_detail', request_method='DELETE', permission=DELETE_PERMISSION, renderer='json')
def delete_product(request):
    """Delete a product"""
    try:
        product_id = request.matchdict['id']
        product = request.dbsession.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return HTTPNotFound(json_body={
                'status': 'error',
                'message': 'Product not found'
            })
        
        request.dbsession.delete(product)
        
        return {
            'status': 'success',
            'message': 'Product deleted successfully'
        }
    except Exception as e:
        request.dbsession.rollback()
        log.error(f"Error in delete_product: {e}")
        return HTTPInternalServerError(json_body={
            'status': 'error',
            'message': 'Server error occurred while deleting product'
        })