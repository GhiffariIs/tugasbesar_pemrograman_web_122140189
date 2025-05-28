from pyramid.view import view_defaults, view_config
from ..models.category import Category
from .base import BaseView
from pyramid.httpexceptions import HTTPNotFound
import json


@view_defaults(route_name='categories', renderer='json')
class CategoryView(BaseView):
    
    @view_config(request_method='GET')
    def get_all_categories(self):
        try:
            categories = self.dbsession.query(Category).all()
            return self.json_response([cat.to_dict() for cat in categories])
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='POST', permission='user')
    def create_category(self):
        try:
            body = self.request.json_body
            nama_kategori = body.get('nama_kategori')
            
            if not nama_kategori:
                return self.error_response("nama_kategori is required", 400)
                
            # Check if category already exists
            existing = self.dbsession.query(Category).filter_by(nama_kategori=nama_kategori).first()
            if existing:
                return self.error_response("Category with this name already exists", 400)
                
            category = Category(nama_kategori=nama_kategori)
            self.dbsession.add(category)
            self.dbsession.flush()
            
            return self.json_response(category.to_dict(), status=201)
        except Exception as e:
            return self.error_response(str(e), 500)


@view_defaults(route_name='category_item', renderer='json')
class CategoryItemView(BaseView):
    
    @view_config(request_method='GET')
    def get_category(self):
        try:
            category_id = int(self.request.matchdict['id'])
            category = self.dbsession.query(Category).filter_by(id=category_id).first()
            
            if not category:
                return self.error_response("Category not found", 404)
                
            return self.json_response(category.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
    
    @view_config(request_method='PUT', permission='user')
    def update_category(self):
        try:
            category_id = int(self.request.matchdict['id'])
            body = self.request.json_body
            nama_kategori = body.get('nama_kategori')
            
            if not nama_kategori:
                return self.error_response("nama_kategori is required", 400)
                
            category = self.dbsession.query(Category).filter_by(id=category_id).first()
            if not category:
                return self.error_response("Category not found", 404)
                
            # Check if new name is already in use by another category
            existing = self.dbsession.query(Category).filter(
                Category.nama_kategori == nama_kategori,
                Category.id != category_id
            ).first()
            
            if existing:
                return self.error_response("Category with this name already exists", 400)
                
            category.nama_kategori = nama_kategori
            
            return self.json_response(category.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='DELETE', permission='user')
    def delete_category(self):
        try:
            category_id = int(self.request.matchdict['id'])
            category = self.dbsession.query(Category).filter_by(id=category_id).first()
            
            if not category:
                return self.error_response("Category not found", 404)
                
            # Check if any products are using this category
            products_count = self.dbsession.execute(
                "SELECT COUNT(*) FROM products WHERE kategori_id = :id", 
                {"id": category_id}
            ).scalar()
            
            if products_count > 0:
                return self.error_response(
                    "Cannot delete this category because it is being used by products",
                    400
                )
                
            self.dbsession.delete(category)
            
            return self.json_response({"message": "Category deleted successfully"})
        except Exception as e:
            return self.error_response(str(e), 500)
