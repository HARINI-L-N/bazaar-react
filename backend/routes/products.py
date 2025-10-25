from flask import Blueprint, request, jsonify
from models import Product, ViewedProduct
from utils import get_current_user, format_error_response, format_success_response
from flask_jwt_extended import jwt_required
import math

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering and pagination"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = {'is_active': True}
        
        if category:
            query['category'] = category
        
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'tags': {'$in': [{'$regex': search, '$options': 'i'}]}}
            ]
        
        if min_price:
            query['price'] = {'$gte': float(min_price)}
        
        if max_price:
            if 'price' in query:
                query['price']['$lte'] = float(max_price)
            else:
                query['price'] = {'$lte': float(max_price)}
        
        # Build sort criteria
        sort_criteria = []
        if sort_by == 'price':
            sort_criteria.append(('price', 1 if sort_order == 'asc' else -1))
        elif sort_by == 'rating':
            sort_criteria.append(('rating', -1 if sort_order == 'desc' else 1))
        else:
            sort_criteria.append(('created_at', -1 if sort_order == 'desc' else 1))
        
        # Get products with pagination
        products = Product.objects(**query).order_by(*sort_criteria).paginate(
            page=page, per_page=per_page
        )
        
        # Convert to dict
        products_data = [product.to_dict() for product in products.items]
        
        return format_success_response({
            'products': products_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get products: {str(e)}", 500)

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details by ID"""
    try:
        product = Product.objects(id=product_id, is_active=True).first()
        if not product:
            return format_error_response("Product not found", 404)
        
        # Track product view if user is authenticated
        try:
            from flask_jwt_extended import get_jwt_identity
            user_id = get_jwt_identity()
            if user_id:
                ViewedProduct(
                    user_id=user_id,
                    product_id=product_id
                ).save()
        except:
            pass  # Continue even if tracking fails
        
        return format_success_response(product.to_dict())
        
    except Exception as e:
        return format_error_response(f"Failed to get product: {str(e)}", 500)

@products_bp.route('/products/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Product.objects(is_active=True).distinct('category')
        return format_success_response(categories)
        
    except Exception as e:
        return format_error_response(f"Failed to get categories: {str(e)}", 500)

@products_bp.route('/products/featured', methods=['GET'])
def get_featured_products():
    """Get featured products (high-rated products)"""
    try:
        limit = int(request.args.get('limit', 8))
        products = Product.objects(
            is_active=True,
            rating__gte=4.0
        ).order_by('-rating', '-review_count').limit(limit)
        
        products_data = [product.to_dict() for product in products]
        return format_success_response(products_data)
        
    except Exception as e:
        return format_error_response(f"Failed to get featured products: {str(e)}", 500)

