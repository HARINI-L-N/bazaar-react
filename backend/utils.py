from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Valid password"

def get_current_user():
    """Get current user from JWT token"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        return user
    except Exception:
        return None

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, "All required fields present"

def calculate_similarity_score(user1_items, user2_items):
    """Calculate similarity score between two users based on viewed products"""
    if not user1_items or not user2_items:
        return 0.0
    
    # Convert to sets for easier comparison
    set1 = set(user1_items)
    set2 = set(user2_items)
    
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return 0.0
    
    return intersection / union

def get_content_similarity(product1, product2):
    """Calculate content-based similarity between two products"""
    score = 0.0
    
    # Category similarity (weight: 0.4)
    if product1.category == product2.category:
        score += 0.4
    
    # Tags similarity (weight: 0.3)
    if product1.tags and product2.tags:
        common_tags = set(product1.tags).intersection(set(product2.tags))
        if product1.tags or product2.tags:
            tag_similarity = len(common_tags) / max(len(product1.tags), len(product2.tags))
            score += 0.3 * tag_similarity
    
    # Features similarity (weight: 0.3)
    if product1.features and product2.features:
        common_features = set(product1.features).intersection(set(product2.features))
        if product1.features or product2.features:
            feature_similarity = len(common_features) / max(len(product1.features), len(product2.features))
            score += 0.3 * feature_similarity
    
    return score

def format_error_response(message, status_code=400):
    """Format error response consistently"""
    return jsonify({'error': message}), status_code

def format_success_response(data, message="Success", status_code=200):
    """Format success response consistently"""
    return jsonify({'data': data, 'message': message}), status_code

