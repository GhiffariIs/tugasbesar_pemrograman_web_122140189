import unittest
from pyramid import testing
import json
from ..models.category import Category
from .base import BaseTest


class CategoryViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test categories
        self.category1 = Category(nama_kategori='Test Category 1')
        self.category2 = Category(nama_kategori='Test Category 2')
        self.session.add(self.category1)
        self.session.add(self.category2)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_all_categories(self):
        from ..views.category import CategoryView
        
        request = testing.DummyRequest(dbsession=self.session)
        view = CategoryView(request)
        response = view.get_all_categories()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(len(body), 2)
        
        # Check that all categories are returned
        categories = [cat['nama_kategori'] for cat in body]
        self.assertIn('Test Category 1', categories)
        self.assertIn('Test Category 2', categories)
    
    def test_create_category(self):
        from ..views.category import CategoryView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'nama_kategori': 'New Category'
            }
        )
        view = CategoryView(request)
        response = view.create_category()
        
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.body)
        self.assertEqual(body['nama_kategori'], 'New Category')
        
        # Check that category was created in database
        category = self.session.query(Category).filter_by(nama_kategori='New Category').first()
        self.assertIsNotNone(category)
    
    def test_create_duplicate_category(self):
        from ..views.category import CategoryView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            json_body={
                'nama_kategori': 'Test Category 1'  # Existing category
            }
        )
        view = CategoryView(request)
        response = view.create_category()
        
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertIn('error', body)
        self.assertIn('already exists', body['error'])


class CategoryItemViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.config.include('..views')
        
        # Add test categories
        self.category1 = Category(nama_kategori='Test Category 1')
        self.category2 = Category(nama_kategori='Test Category 2')
        self.session.add(self.category1)
        self.session.add(self.category2)
        self.session.flush()
    
    def tearDown(self):
        super().tearDown()
    
    def test_get_category(self):
        from ..views.category import CategoryItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.category1.id}
        )
        view = CategoryItemView(request)
        response = view.get_category()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(body['nama_kategori'], 'Test Category 1')
    
    def test_get_nonexistent_category(self):
        from ..views.category import CategoryItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': 9999}  # Nonexistent ID
        )
        view = CategoryItemView(request)
        response = view.get_category()
        
        self.assertEqual(response.status_code, 404)
        body = json.loads(response.body)
        self.assertIn('error', body)
    
    def test_update_category(self):
        from ..views.category import CategoryItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.category1.id},
            json_body={
                'nama_kategori': 'Updated Category'
            }
        )
        view = CategoryItemView(request)
        response = view.update_category()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertEqual(body['nama_kategori'], 'Updated Category')
        
        # Check that category was updated in database
        category = self.session.query(Category).get(self.category1.id)
        self.assertEqual(category.nama_kategori, 'Updated Category')
    
    def test_delete_category(self):
        from ..views.category import CategoryItemView
        
        request = testing.DummyRequest(
            dbsession=self.session,
            matchdict={'id': self.category1.id}
        )
        view = CategoryItemView(request)
        response = view.delete_category()
        
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.body)
        self.assertIn('message', body)
        
        # Check that category was deleted from database
        category = self.session.query(Category).get(self.category1.id)
        self.assertIsNone(category)
