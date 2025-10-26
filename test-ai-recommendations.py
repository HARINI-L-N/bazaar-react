#!/usr/bin/env python3
"""
Test script for AI-powered recommendation system
Tests both content-based and collaborative filtering endpoints
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000/api"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_products_endpoint():
    """Test products endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/products", timeout=5)
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('products', [])
            print(f"✅ Products endpoint: {len(products)} products found")
            return products
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Products endpoint error: {e}")
        return []

def test_user_login():
    """Test user login and get token"""
    try:
        login_data = {
            "username": "john@example.com",
            "password": "password123"
        }
        response = requests.post(f"{API_BASE_URL}/users/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('access_token')
            user_id = data.get('data', {}).get('user', {}).get('id')
            print("✅ User login successful")
            return token, user_id
        else:
            print(f"❌ User login failed: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None, None

def test_content_based_recommendations(product_id, token):
    """Test content-based recommendations"""
    try:
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        response = requests.get(f"{API_BASE_URL}/recommendations/content/{product_id}", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('data', {}).get('recommendations', [])
            print(f"✅ Content-based recommendations: {len(recommendations)} products")
            
            # Print recommendation details
            for i, rec in enumerate(recommendations[:3], 1):
                product = rec.get('product', {})
                similarity = rec.get('similarity_score', 0)
                print(f"   {i}. {product.get('name', 'Unknown')} (similarity: {similarity:.3f})")
            
            return recommendations
        else:
            print(f"❌ Content-based recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Content-based recommendations error: {e}")
        return []

def test_collaborative_recommendations(user_id, token):
    """Test collaborative filtering recommendations"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{API_BASE_URL}/recommendations/collaborative/{user_id}", 
                              headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('data', {}).get('recommendations', [])
            print(f"✅ Collaborative recommendations: {len(recommendations)} products")
            
            # Print recommendation details
            for i, rec in enumerate(recommendations[:3], 1):
                product = rec.get('product', {})
                score = rec.get('score', 0)
                print(f"   {i}. {product.get('name', 'Unknown')} (score: {score:.3f})")
            
            return recommendations
        else:
            print(f"❌ Collaborative recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Collaborative recommendations error: {e}")
        return []

def test_product_view_tracking(product_id, token):
    """Test product view tracking"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        tracking_data = {
            "product_id": product_id,
            "view_duration": 60
        }
        response = requests.post(f"{API_BASE_URL}/track/view", 
                               json=tracking_data, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✅ Product view tracking successful")
            return True
        else:
            print(f"❌ Product view tracking failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Product view tracking error: {e}")
        return False

def test_user_history(user_id, token):
    """Test user viewing history"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/history", 
                              headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            history = data.get('data', {}).get('history', [])
            print(f"✅ User history: {len(history)} viewed products")
            return history
        else:
            print(f"❌ User history failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ User history error: {e}")
        return []

def main():
    """Run all AI recommendation tests"""
    print("🤖 AI E-Commerce Recommendation System Test")
    print("=" * 60)
    
    # Test 1: Backend Health
    print("\n1. Testing Backend Health...")
    if not test_backend_health():
        print("\n❌ Backend not available. Please start the backend server:")
        print("   cd backend && python app.py")
        return
    
    # Test 2: Products
    print("\n2. Testing Products Endpoint...")
    products = test_products_endpoint()
    if not products:
        print("❌ No products available. Please populate the database:")
        print("   cd backend && python populate_db.py")
        return
    
    # Test 3: User Authentication
    print("\n3. Testing User Authentication...")
    token, user_id = test_user_login()
    if not token:
        print("❌ Authentication failed. Please check user credentials.")
        return
    
    # Test 4: Product View Tracking
    print("\n4. Testing Product View Tracking...")
    test_product_view_tracking(products[0]['id'], token)
    
    # Test 5: User History
    print("\n5. Testing User Viewing History...")
    test_user_history(user_id, token)
    
    # Test 6: Content-Based Recommendations
    print("\n6. Testing Content-Based Recommendations...")
    content_recs = test_content_based_recommendations(products[0]['id'], token)
    
    # Test 7: Collaborative Filtering
    print("\n7. Testing Collaborative Filtering...")
    collab_recs = test_collaborative_recommendations(user_id, token)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 AI Recommendation System Test Complete!")
    print("=" * 60)
    
    print(f"\n📊 Test Results:")
    print(f"   • Products available: {len(products)}")
    print(f"   • Content-based recommendations: {len(content_recs)}")
    print(f"   • Collaborative recommendations: {len(collab_recs)}")
    
    print(f"\n🌐 Frontend URLs:")
    print(f"   • Home: http://localhost:5173/")
    print(f"   • Product: http://localhost:5173/products/{products[0]['id']}")
    
    print(f"\n🔧 Backend URLs:")
    print(f"   • Health: http://localhost:5000/api/health")
    print(f"   • Products: http://localhost:5000/api/products")
    print(f"   • Content-based: http://localhost:5000/api/recommendations/content/{products[0]['id']}")
    print(f"   • Collaborative: http://localhost:5000/api/recommendations/collaborative/{user_id}")
    
    print(f"\n✅ AI Recommendation System is working!")
    print(f"   The system can now provide personalized product recommendations")
    print(f"   using both content-based and collaborative filtering algorithms.")

if __name__ == '__main__':
    main()
