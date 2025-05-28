from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPForbidden
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from ..models import DBSession
from ..models.product import Product
from ..models.category import Category
from .base import BaseView

@view_defaults(renderer='json', permission='view')
class ProductViews(BaseView):
    """Product views."""
    
    @view_config(route_name='products', request_method='GET')
    def list_products(self):
        """List all products with optional filtering."""
        query = DBSession.query(Product)
        
        # Filter by category
        category_id = self.request.params.get('category_id')
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        # Search
        search = self.request.params.get('q')
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.sku.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Sort
        sort_by = self.request.params.get('sort_by', 'name')
        sort_dir = self.request.params.get('sort_dir', 'asc')
        
        if sort_dir == 'desc':
            query = query.order_by(getattr(Product, sort_by).desc())
        else:
            query = query.order_by(getattr(Product, sort_by).asc())
        
        # Pagination
        page = int(self.request.params.get('page', 1))
        limit = int(self.request.params.get('limit', 20))
        offset = (page - 1) * limit
        
        total = query.count()
        products = query.limit(limit).offset(offset).all()
        
        return {
            'products': [product.to_dict() for product in products],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        }
    
    @view_config(route_name='product', request_method='GET')
    def get_product(self):
        """Get a single product."""
        product_id = self.request.matchdict['id']
        product = DBSession.query(Product).get(product_id)
        
        if not product:
            return HTTPNotFound(json_body={
                'status': 'error',
                'message': f'Product with id {product_id} not found'
            })
            
        return product.to_dict()
    
    @view_config(route_name='product_search', request_method='GET')
    def search_products(self):
        """Search products."""
        search = self.request.params.get('q', '')
        if not search:
            return self.list_products()
            
        search_term = f'%{search}%'
        query = DBSession.query(Product).filter(
            or_(
                Product.name.ilike(search_term),
                Product.sku.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
        
        products = query.all()
        
        return {
            'products': [product.to_dict() for product in products],
        }
    
    @view_config(route_name='low_stock_products', request_method='GET')
    def low_stock_products(self):
        """Get products with low stock."""
        query = DBSession.query(Product)
        query = query.filter(Product.stock_quantity <= Product.minimum_stock)
        products = query.all()
        
        return {
            'products': [product.to_dict() for product in products],
        }
    
    @view_config(route_name='products', request_method='POST')
    def create_product(self):
        """Create a new product."""
        try:
            body = self._get_json_body()
            name = body.get('name')
            sku = body.get('sku')
            description = body.get('description')
            price = body.get('price')
            stock_quantity = body.get('stock_quantity', 0)
            minimum_stock = body.get('minimum_stock', 5)
            category_id = body.get('category_id')
            
            if not all([name, sku, price, category_id]):
                return HTTPBadRequest(json_body={
                    'status': 'error',
                    'message': 'Name, SKU, price, and category_id are required'
                })
            
            # Check if the category exists
            category = DBSession.query(Category).get(category_id)
            if not category:
                return HTTPBadRequest(json_body={
                    'status': 'error',
                    'message': f'Category with id {category_id} not found'
                })
            
            product = Product(
                name=name,
                sku=sku,
                description=description,
                price=float(price),
                stock_quantity=int(stock_quantity),
                minimum_stock=int(minimum_stock),
                category_id=category_id,
                created_by=self.request.user.id
            )
            
            DBSession.add(product)
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Product created successfully',
                'product': product.to_dict()
            }
        except IntegrityError:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A product with that SKU already exists'
            })
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
    
    @view_config(route_name='product', request_method='PUT')
    def update_product(self):
        """Update a product."""
        try:
            product_id = self.request.matchdict['id']
            product = DBSession.query(Product).get(product_id)
            
            if not product:
                return HTTPNotFound(json_body={
                    'status': 'error',
                    'message': f'Product with id {product_id} not found'
                })
            
            body = self._get_json_body()
            
            # Update fields
            for field in ['name', 'sku', 'description', 'price', 'stock_quantity', 'minimum_stock', 'category_id']:
                if field in body:
                    value = body.get(field)
                    if field in ['price']:
                        value = float(value)
                    elif field in ['stock_quantity', 'minimum_stock', 'category_id']:
                        value = int(value)
                    
                    setattr(product, field, value)
            
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Product updated successfully',
                'product': product.to_dict()
            }
        except IntegrityError:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A product with that SKU already exists'
            })
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
    
    @view_config(route_name='product', request_method='DELETE')
    def delete_product(self):
        """Delete a product."""
        try:
            product_id = self.request.matchdict['id']
            product = DBSession.query(Product).get(product_id)
            
            if not product:
                return HTTPNotFound(json_body={
                    'status': 'error',
                    'message': f'Product with id {product_id} not found'
                })
            
            DBSession.delete(product)
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Product deleted successfully'
            }
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
