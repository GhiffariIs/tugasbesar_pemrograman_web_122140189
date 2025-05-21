import unittest
from pyramid import testing
import json
from ..models.product import Product
from ..models.category import Category
from .base import BaseTest


class ProductViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
        
        # Add test products
        self.product1 = Product(
            nama_produk='Test Product 1',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description 1'
        )
        self.product2 = Product(
            nama_produk='Test Product 2',
            kategori_id=self.category.id,
            stok=20,
            harga=20000,
            deskripsi='Test Description 2'
        )
        self.session.add(self.product1)
        self.session.add(self.product2)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_all_products(self):
        from ..views.product import ProductView
        
        request = testing.DummyRequest(dbsession=self.session)
        view = ProductView(request)
        response = view.get_all_products()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(len(body), 2)
        
        # Check that both products are returned
        products = [prod['nama_produk'] for prod in body]
        self.assertIn('Test Product 1', products)
        self.assertIn('Test Product 2', products)
    
    def test_create_product(self):
        from ..views.product import ProductView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'nama_produk': 'New Product',
                'kategori_id': self.category.id,
                'stok': 15,
                'harga': 15000,
                'deskripsi': 'New Product Description'
            }
        )
        view = ProductView(request)
        response = view.create_product()
        
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.body)
        self.assertEqual(body['nama_produk'], 'New Product')
        self.assertEqual(body['stok'], 15)
        self.assertEqual(body['harga'], 15000)
        
        # Check that product was created in database
        product = self.session.query(Product).filter_by(nama_produk='New Product').first()
        self.assertIsNotNone(product)
    
    def test_create_product_invalid_category(self):
        from ..views.product import ProductView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'nama_produk': 'New Product',
                'kategori_id': 9999,  # Nonexistent category
                'stok': 15,
                'harga': 15000,
                'deskripsi': 'New Product Description'
            }
        )
        view = ProductView(request)
        response = view.create_product()
        
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertIn('error', body)
        self.assertIn('Category not found', body['error'])


class ProductItemViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
        
        # Add test product
        self.product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(self.product)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_product(self):
        from ..views.product import ProductItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.product.id}
        )
        view = ProductItemView(request)
        response = view.get_product()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(body['nama_produk'], 'Test Product')
        self.assertEqual(body['stok'], 10)
        self.assertEqual(body['harga'], 10000)
    
    def test_get_nonexistent_product(self):
        from ..views.product import ProductItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': 9999}  # Nonexistent ID
        )
        view = ProductItemView(request)
        response = view.get_product()
        
        self.assertEqual(response.status_code, 404)
        body = json.loads(response.body)
        self.assertIn('error', body)
    
    def test_update_product(self):
        from ..views.product import ProductItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.product.id},
            json_body={
                'nama_produk': 'Updated Product',
                'stok': 15,
                'harga': 15000
            }
        )
        view = ProductItemView(request)
        response = view.update_product()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(body['nama_produk'], 'Updated Product')
        self.assertEqual(body['stok'], 15)
        self.assertEqual(body['harga'], 15000)
        
        # Check that product was updated in database
        product = self.session.query(Product).get(self.product.id)
        self.assertEqual(product.nama_produk, 'Updated Product')
        self.assertEqual(product.stok, 15)
        self.assertEqual(product.harga, 15000)
    
    def test_delete_product(self):
        from ..views.product import ProductItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.product.id}
        )
        view = ProductItemView(request)
        response = view.delete_product()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertIn('message', body)
        
        # Check that product was deleted from database
        product = self.session.query(Product).get(self.product.id)
        self.assertIsNone(product)
