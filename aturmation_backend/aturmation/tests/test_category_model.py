import unittest
import transaction
from pyramid import testing
from ..models.category import Category
from .base import BaseTest


class CategoryModelTest(BaseTest):
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
    
    def test_category_creation(self):
        category = Category(nama_kategori='Test Category')
        self.session.add(category)
        self.session.flush()
        
        self.assertEqual(category.nama_kategori, 'Test Category')
        
    def test_to_dict(self):
        category = Category(nama_kategori='Test Category')
        self.session.add(category)
        self.session.flush()
        
        category_dict = category.to_dict()
        self.assertEqual(category_dict['nama_kategori'], 'Test Category')
        self.assertIn('id', category_dict)
