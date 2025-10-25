#!/usr/bin/env python3
"""
Integration test script to verify backend and frontend are working
"""

import requests
import time
import json

def test_backend():
    """Test backend API endpoints"""
    print("🧪 Testing Backend API...")
    
    base_url = "http://localhost:5000/api"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: OK")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False
    
    # Test products endpoint
    try:
        response = requests.get(f"{base_url}/products", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'products' in data['data']:
                print(f"✅ Products API: {len(data['data']['products'])} products found")
            else:
                print("❌ Products API: Invalid response format")
                return False
        else:
            print(f"❌ Products API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Products API error: {e}")
        return False
    
    # Test categories endpoint
    try:
        response = requests.get(f"{base_url}/products/categories", timeout=5)
        if response.status_code == 200:
            print("✅ Categories API: OK")
        else:
            print(f"❌ Categories API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Categories API error: {e}")
        return False
    
    return True

def test_frontend():
    """Test frontend server"""
    print("\n🧪 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:5173/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server: Running on port 5173")
            return True
        else:
            print(f"❌ Frontend server failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend not running on port 5173")
        return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n🧪 Testing User Registration...")
    
    base_url = "http://localhost:5000/api"
    
    # Test user registration
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(
            f"{base_url}/users/register",
            json=user_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            if 'data' in data and 'access_token' in data['data']:
                print("✅ User registration: Success")
                return data['data']['access_token']
            else:
                print("❌ User registration: Invalid response")
                return None
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return None

def test_authenticated_endpoints(token):
    """Test authenticated endpoints"""
    print("\n🧪 Testing Authenticated Endpoints...")
    
    base_url = "http://localhost:5000/api"
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test cart endpoint
    try:
        response = requests.get(f"{base_url}/cart", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Cart API: OK")
        else:
            print(f"❌ Cart API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cart API error: {e}")
    
    # Test orders endpoint
    try:
        response = requests.get(f"{base_url}/orders", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Orders API: OK")
        else:
            print(f"❌ Orders API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Orders API error: {e}")

def main():
    """Run all tests"""
    print("🚀 E-commerce Integration Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend()
    if not backend_ok:
        print("\n❌ Backend tests failed. Please check:")
        print("1. MongoDB is running")
        print("2. Backend server is running: python app.py")
        print("3. Database is populated: python populate_db.py")
        return
    
    # Test frontend
    frontend_ok = test_frontend()
    if not frontend_ok:
        print("\n❌ Frontend tests failed. Please check:")
        print("1. Frontend server is running: npm run dev")
        print("2. No port conflicts")
        return
    
    # Test user registration
    token = test_user_registration()
    if token:
        test_authenticated_endpoints(token)
    
    print("\n" + "=" * 50)
    print("🎉 Integration Test Complete!")
    print("=" * 50)
    print("\n✅ Backend: http://localhost:5000")
    print("✅ Frontend: http://localhost:5173")
    print("\n📝 Test Credentials:")
    print("- john@example.com / password123")
    print("- jane@example.com / password123")
    print("- admin@example.com / admin123")
    print("\n🧪 Manual Tests:")
    print("1. Open http://localhost:5173/")
    print("2. Check products load from backend")
    print("3. Try logging in with test credentials")
    print("4. Add items to cart")
    print("5. Create an order")

if __name__ == '__main__':
    main()
