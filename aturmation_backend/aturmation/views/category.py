from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPForbidden
from sqlalchemy.exc import IntegrityError

from ..models import DBSession
from ..models.category import Category
from .base import BaseView

@view_defaults(renderer='json', permission='view')
class CategoryViews(BaseView):
    """Category views."""
    
    @view_config(route_name='categories', request_method='GET')
    def list_categories(self):
        """List all categories."""
        categories = DBSession.query(Category).all()
        return {'categories': [category.to_dict() for category in categories]}
    
    @view_config(route_name='category', request_method='GET')
    def get_category(self):
        """Get a single category."""
        category_id = self.request.matchdict['id']
        category = DBSession.query(Category).get(category_id)
        
        if not category:
            return HTTPNotFound(json_body={
                'status': 'error',
                'message': f'Category with id {category_id} not found'
            })
            
        return category.to_dict()
    
    @view_config(route_name='categories', request_method='POST')
    def create_category(self):
        """Create a new category."""
        try:
            body = self._get_json_body()
            name = body.get('name')
            description = body.get('description')
            
            if not name:
                return HTTPBadRequest(json_body={
                    'status': 'error',
                    'message': 'Name is required'
                })
            
            category = Category(
                name=name,
                description=description,
                created_by=self.request.user.id
            )
            
            DBSession.add(category)
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Category created successfully',
                'category': category.to_dict()
            }
        except IntegrityError:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A category with that name already exists'
            })
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
    
    @view_config(route_name='category', request_method='PUT')
    def update_category(self):
        """Update a category."""
        try:
            category_id = self.request.matchdict['id']
            category = DBSession.query(Category).get(category_id)
            
            if not category:
                return HTTPNotFound(json_body={
                    'status': 'error',
                    'message': f'Category with id {category_id} not found'
                })
            
            body = self._get_json_body()
            name = body.get('name')
            description = body.get('description')
            
            if name:
                category.name = name
            
            if description is not None:  # Allow empty description
                category.description = description
            
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Category updated successfully',
                'category': category.to_dict()
            }
        except IntegrityError:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': 'A category with that name already exists'
            })
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
    
    @view_config(route_name='category', request_method='DELETE')
    def delete_category(self):
        """Delete a category."""
        try:
            category_id = self.request.matchdict['id']
            category = DBSession.query(Category).get(category_id)
            
            if not category:
                return HTTPNotFound(json_body={
                    'status': 'error',
                    'message': f'Category with id {category_id} not found'
                })
            
            # Check if the category has products
            if category.products:
                return HTTPBadRequest(json_body={
                    'status': 'error',
                    'message': 'Cannot delete category with products'
                })
            
            DBSession.delete(category)
            DBSession.flush()
            
            return {
                'status': 'success',
                'message': 'Category deleted successfully'
            }
        except Exception as e:
            DBSession.rollback()
            return HTTPBadRequest(json_body={
                'status': 'error',
                'message': str(e)
            })
