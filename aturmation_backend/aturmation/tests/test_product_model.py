import unittest
import transaction
from pyramid import testing
from ..models.product import Product
from ..models.category import Category
from .base import BaseTest


class ProductModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        
        # Add a test category
        self.category = Category(nama_kategori='Test Category')
        self.session.add(self.category)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_product_creation(self):
        product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(product)
        self.session.flush()
        
        self.assertEqual(product.nama_produk, 'Test Product')
        self.assertEqual(product.kategori_id, self.category.id)
        self.assertEqual(product.stok, 10)
        self.assertEqual(product.harga, 10000)
        self.assertEqual(product.deskripsi, 'Test Description')
        
    def test_to_dict(self):
        product = Product(
            nama_produk='Test Product',
            kategori_id=self.category.id,
            stok=10,
            harga=10000,
            deskripsi='Test Description'
        )
        self.session.add(product)
        self.session.flush()
        
        product_dict = product.to_dict()
        self.assertEqual(product_dict['nama_produk'], 'Test Product')
        self.assertEqual(product_dict['kategori_id'], self.category.id)
        self.assertEqual(product_dict['stok'], 10)
        self.assertEqual(product_dict['harga'], 10000)
        self.assertEqual(product_dict['deskripsi'], 'Test Description')
        self.assertEqual(product_dict['kategori_nama'], 'Test Category')
