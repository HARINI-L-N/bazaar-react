#!/usr/bin/env python3
"""
Script to populate the database with sample data for testing
Run this script after setting up the Flask app to create sample users and products
"""

import os
import sys
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Product, ViewedProduct, Cart, CartItem, Order, OrderItem
from seeds.user_seeds import users_data
from seeds.product_seeds import products_data

def create_sample_data():
    """Create sample data for testing"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        User.objects.delete()
        Product.objects.delete()
        ViewedProduct.objects.delete()
        Cart.objects.delete()
        Order.objects.delete()
        
        print("Creating sample users...")
        
        # Create sample users from seeds
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.set_password(user_data['password'])
            user.save()
            users.append(user)
            print(f"Created user: {user.username}")
        
        print("Creating sample products...")
        
        # Create sample products from seeds
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            product.save()
            products.append(product)
            print(f"Created product: {product.name}")
        
        print("Creating sample user interactions...")
        
        # Create some sample viewed products for users
        sample_views = [
            (users[0].id, products[0].id, 120),  # John viewed headphones for 2 minutes
            (users[0].id, products[1].id, 90),   # John viewed smartwatch for 1.5 minutes
            (users[0].id, products[2].id, 45),    # John viewed t-shirt for 45 seconds
            (users[1].id, products[0].id, 180),   # Jane viewed headphones for 3 minutes
            (users[1].id, products[3].id, 60),    # Jane viewed water bottle for 1 minute
            (users[1].id, products[4].id, 75),    # Jane viewed charging pad for 1.25 minutes
            (users[1].id, products[5].id, 150),   # Jane viewed yoga mat for 2.5 minutes
        ]
        
        for user_id, product_id, duration in sample_views:
            viewed_product = ViewedProduct(
                user_id=user_id,
                product_id=product_id,
                view_duration=duration
            )
            viewed_product.save()
        
        print("Creating sample cart for John...")
        
        # Create sample cart for John
        john_cart = Cart(user_id=users[0].id)
        john_cart.items = [
            CartItem(product_id=products[0].id, quantity=1),
            CartItem(product_id=products[2].id, quantity=2)
        ]
        john_cart.save()
        
        print("Creating sample order for Jane...")
        
        # Create sample order for Jane
        jane_order = Order(
            user_id=users[1].id,
            items=[
                OrderItem(
                    product_id=products[0].id,
                    product_name=products[0].name,
                    quantity=1,
                    price=products[0].price
                ),
                OrderItem(
                    product_id=products[3].id,
                    product_name=products[3].name,
                    quantity=2,
                    price=products[3].price
                )
            ],
            total_amount=products[0].price + (products[3].price * 2),
            shipping_address={
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'country': 'USA'
            },
            payment_method='credit_card',
            status='delivered'
        )
        jane_order.save()
        
        print("\n" + "="*50)
        print("Sample data created successfully!")
        print("="*50)
        print(f"Users created: {len(users)}")
        print(f"Products created: {len(products)}")
        print(f"Sample views created: {len(sample_views)}")
        print(f"Sample cart created for: {users[0].username}")
        print(f"Sample order created for: {users[1].username}")
        print("\nTest credentials:")
        print("John Doe: john@example.com / password123")
        print("Jane Smith: jane@example.com / password123")
        print("Admin: admin@example.com / admin123")
        print("="*50)

if __name__ == '__main__':
    create_sample_data()

