from pyramid.view import view_defaults, view_config
from ..models.product import Product
from ..models.category import Category
from .base import BaseView
from pyramid.httpexceptions import HTTPNotFound
import json


@view_defaults(route_name='products', renderer='json')
class ProductView(BaseView):
    
    @view_config(request_method='GET')
    def get_all_products(self):
        try:
            products = self.dbsession.query(Product).all()
            return self.json_response([prod.to_dict() for prod in products])
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='POST', permission='user')
    def create_product(self):
        try:
            body = self.request.json_body
            nama_produk = body.get('nama_produk')
            kategori_id = body.get('kategori_id')
            stok = body.get('stok', 0)
            harga = body.get('harga')
            deskripsi = body.get('deskripsi', '')
            
            if not nama_produk or not kategori_id or harga is None:
                return self.error_response(
                    "nama_produk, kategori_id, and harga are required fields", 
                    400
                )
            
            # Check if category exists
            category = self.dbsession.query(Category).filter_by(id=kategori_id).first()
            if not category:
                return self.error_response("Category not found", 400)
                
            product = Product(
                nama_produk=nama_produk,
                kategori_id=kategori_id,
                stok=stok,
                harga=harga,
                deskripsi=deskripsi
            )
            
            self.dbsession.add(product)
            self.dbsession.flush()
            
            return self.json_response(product.to_dict(), status=201)
        except Exception as e:
            return self.error_response(str(e), 500)


@view_defaults(route_name='product_item', renderer='json')
class ProductItemView(BaseView):
    
    @view_config(request_method='GET')
    def get_product(self):
        try:
            product_id = int(self.request.matchdict['id'])
            product = self.dbsession.query(Product).filter_by(id=product_id).first()
            
            if not product:
                return self.error_response("Product not found", 404)
                
            return self.json_response(product.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
    
    @view_config(request_method='PUT', permission='user')
    def update_product(self):
        try:
            product_id = int(self.request.matchdict['id'])
            body = self.request.json_body
            
            product = self.dbsession.query(Product).filter_by(id=product_id).first()
            if not product:
                return self.error_response("Product not found", 404)
            
            # Update fields if they are present
            if 'nama_produk' in body:
                product.nama_produk = body['nama_produk']
                
            if 'kategori_id' in body:
                # Check if category exists
                category = self.dbsession.query(Category).filter_by(id=body['kategori_id']).first()
                if not category:
                    return self.error_response("Category not found", 400)
                product.kategori_id = body['kategori_id']
                
            if 'stok' in body:
                product.stok = body['stok']
                
            if 'harga' in body:
                product.harga = body['harga']
                
            if 'deskripsi' in body:
                product.deskripsi = body['deskripsi']
            
            return self.json_response(product.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='DELETE', permission='user')
    def delete_product(self):
        try:
            product_id = int(self.request.matchdict['id'])
            product = self.dbsession.query(Product).filter_by(id=product_id).first()
            
            if not product:
                return self.error_response("Product not found", 404)
                
            # Check if any transactions reference this product
            transactions_count = self.dbsession.execute(
                "SELECT COUNT(*) FROM transactions WHERE produk_id = :id", 
                {"id": product_id}
            ).scalar()
            
            if transactions_count > 0:
                return self.error_response(
                    "Cannot delete this product because it is referenced by transactions",
                    400
                )
                
            self.dbsession.delete(product)
            
            return self.json_response({"message": "Product deleted successfully"})
        except Exception as e:
            return self.error_response(str(e), 500)
