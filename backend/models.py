from flask_mongoengine import MongoEngine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import json

# Initialize MongoDB
db = MongoEngine()

class User(db.Document):
    username = db.StringField(required=True, unique=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Product(db.Document):
    name = db.StringField(required=True, max_length=200)
    description = db.StringField(required=True)
    price = db.FloatField(required=True)
    category = db.StringField(required=True, max_length=100)
    tags = db.ListField(db.StringField(), default=list)
    features = db.ListField(db.StringField(), default=list)
    image_url = db.StringField()
    stock_quantity = db.IntField(default=0)
    rating = db.FloatField(default=0.0)
    review_count = db.IntField(default=0)
    is_active = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'tags': self.tags,
            'features': self.features,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'rating': self.rating,
            'review_count': self.review_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CartItem(db.EmbeddedDocument):
    product_id = db.ObjectIdField(required=True)
    quantity = db.IntField(required=True, min_value=1)
    added_at = db.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'product_id': str(self.product_id),
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat()
        }

class Cart(db.Document):
    user_id = db.ObjectIdField(required=True)
    items = db.ListField(db.EmbeddedDocumentField(CartItem), default=list)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OrderItem(db.EmbeddedDocument):
    product_id = db.ObjectIdField(required=True)
    product_name = db.StringField(required=True)
    quantity = db.IntField(required=True)
    price = db.FloatField(required=True)
    
    def to_dict(self):
        return {
            'product_id': str(self.product_id),
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': self.price
        }

class Order(db.Document):
    user_id = db.ObjectIdField(required=True)
    items = db.ListField(db.EmbeddedDocumentField(OrderItem), required=True)
    total_amount = db.FloatField(required=True)
    status = db.StringField(required=True, choices=['pending', 'processing', 'shipped', 'delivered', 'cancelled'], default='pending')
    shipping_address = db.DictField(required=True)
    payment_method = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'items': [item.to_dict() for item in self.items],
            'total_amount': self.total_amount,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ViewedProduct(db.Document):
    user_id = db.ObjectIdField(required=True)
    product_id = db.ObjectIdField(required=True)
    viewed_at = db.DateTimeField(default=datetime.utcnow)
    view_duration = db.IntField(default=0)  # in seconds
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'product_id': str(self.product_id),
            'viewed_at': self.viewed_at.isoformat(),
            'view_duration': self.view_duration
        }

