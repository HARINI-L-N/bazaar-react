from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
from utils import validate_email, validate_password, get_current_user, validate_required_fields, format_error_response, format_success_response
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return format_error_response(message)
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            return format_error_response("Invalid email format")
        
        # Validate password
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            return format_error_response(password_message)
        
        # Check if user already exists
        if User.objects(username=username).first():
            return format_error_response("Username already exists")
        
        if User.objects(email=email).first():
            return format_error_response("Email already exists")
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        user.set_password(password)
        user.save()
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return format_success_response({
            'user': user.to_dict(),
            'access_token': access_token
        }, "User registered successfully", 201)
        
    except Exception as e:
        return format_error_response(f"Registration failed: {str(e)}", 500)

@auth_bp.route('/users/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'password']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return format_error_response(message)
        
        username = data['username'].strip()
        password = data['password']
        
        # Find user by username or email
        user = User.objects(username=username).first()
        if not user:
            user = User.objects(email=username).first()
        
        if not user or not user.check_password(password):
            return format_error_response("Invalid credentials", 401)
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return format_success_response({
            'user': user.to_dict(),
            'access_token': access_token
        }, "Login successful")
        
    except Exception as e:
        return format_error_response(f"Login failed: {str(e)}", 500)

@auth_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        return format_success_response(user.to_dict())
        
    except Exception as e:
        return format_error_response(f"Failed to get profile: {str(e)}", 500)

@auth_bp.route('/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            email = data['email'].strip().lower()
            if not validate_email(email):
                return format_error_response("Invalid email format")
            if User.objects(email=email).exclude(id=user.id).first():
                return format_error_response("Email already exists")
            user.email = email
        
        user.updated_at = datetime.utcnow()
        user.save()
        
        return format_success_response(user.to_dict(), "Profile updated successfully")
        
    except Exception as e:
        return format_error_response(f"Failed to update profile: {str(e)}", 500)

