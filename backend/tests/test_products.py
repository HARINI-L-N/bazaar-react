"""Tests for Products API"""
import unittest
import json
from app import create_app
from models import db, Product

class ProductsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['MONGODB_URI'] = 'mongodb://localhost:27017/test_db'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        Product.objects.delete()
        self.app_context.pop()
    
    def test_get_products(self):
        """Test getting all products"""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
    
    def test_get_product_by_id(self):
        """Test getting product by ID"""
        # Create a test product
        product = Product(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category="Electronics"
        )
        product.save()
        
        response = self.client.get(f'/api/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data']['name'], "Test Product")
    
    def test_get_categories(self):
        """Test getting categories"""
        response = self.client.get('/api/products/categories')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list)
    
    def test_get_featured_products(self):
        """Test getting featured products"""
        response = self.client.get('/api/products/featured')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['data'], list)

if __name__ == '__main__':
    unittest.main()
