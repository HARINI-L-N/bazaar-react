#!/usr/bin/env python3
"""
Simple API test script to verify all endpoints are working
Run this after starting the Flask application
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print(f"✗ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✓ {method} {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"✗ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"  Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ {method} {endpoint} - Connection failed (Is the server running?)")
        return False
    except Exception as e:
        print(f"✗ {method} {endpoint} - Error: {e}")
        return False

def main():
    print("🧪 Testing E-commerce API Endpoints")
    print("=" * 50)
    
    # Test health check
    print("\n1. Testing health check...")
    test_endpoint('GET', '/health')
    
    # Test product endpoints (no auth required)
    print("\n2. Testing product endpoints...")
    test_endpoint('GET', '/products')
    test_endpoint('GET', '/products/categories')
    test_endpoint('GET', '/products/featured')
    
    # Test user registration
    print("\n3. Testing user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    test_endpoint('POST', '/users/register', user_data, expected_status=201)
    
    # Test user login
    print("\n4. Testing user login...")
    login_data = {
        "username": "test@example.com",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get('data', {}).get('access_token')
        if token:
            print("✓ Login successful, got JWT token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test authenticated endpoints
            print("\n5. Testing authenticated endpoints...")
            test_endpoint('GET', '/users/profile', headers=headers)
            test_endpoint('GET', '/cart', headers=headers)
            test_endpoint('GET', '/orders', headers=headers)
            
            # Test adding to cart
            print("\n6. Testing cart operations...")
            cart_data = {
                "product_id": "507f1f77bcf86cd799439011",  # This will fail, but tests the endpoint
                "quantity": 1
            }
            test_endpoint('POST', '/cart', cart_data, headers=headers, expected_status=404)  # Expected to fail due to invalid product ID
            
            # Test tracking
            print("\n7. Testing tracking...")
            track_data = {
                "product_id": "507f1f77bcf86cd799439011",
                "view_duration": 60
            }
            test_endpoint('POST', '/track/view', track_data, headers=headers, expected_status=404)  # Expected to fail due to invalid product ID
            
        else:
            print("✗ No token in login response")
    else:
        print(f"✗ Login failed: {response.status_code}")
    
    # Test with existing sample users
    print("\n8. Testing with sample users...")
    sample_login = {
        "username": "john@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/login", json=sample_login)
    
    if response.status_code == 200:
        token = response.json().get('data', {}).get('access_token')
        if token:
            print("✓ Sample user login successful")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test recommendations
            print("\n9. Testing recommendations...")
            user_id = response.json().get('data', {}).get('user', {}).get('id')
            if user_id:
                test_endpoint('GET', f'/recommendations/{user_id}', headers=headers)
                test_endpoint('GET', f'/users/{user_id}/history', headers=headers)
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("=" * 50)
    print("\nNote: Some tests may fail if the database is empty.")
    print("Run 'python populate_db.py' to create sample data first.")

if __name__ == '__main__':
    main()

