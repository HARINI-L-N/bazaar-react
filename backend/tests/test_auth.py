"""Tests for Authentication API"""
import unittest
import json
from app import create_app
from models import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['MONGODB_URI'] = 'mongodb://localhost:27017/test_db'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        User.objects.delete()
        self.app_context.pop()
    
    def test_register_user(self):
        """Test user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/api/users/register', 
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data_response = json.loads(response.data)
        self.assertIn('access_token', data_response['data'])
    
    def test_login_user(self):
        """Test user login"""
        # Create a test user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('testpass123')
        user.save()
        
        data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data_response = json.loads(response.data)
        self.assertIn('access_token', data_response['data'])
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/users/login',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
