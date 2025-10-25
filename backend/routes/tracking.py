from flask import Blueprint, request, jsonify
from models import ViewedProduct, Product, User
from utils import get_current_user, format_error_response, format_success_response
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track/view', methods=['POST'])
@jwt_required()
def track_product_view():
    """Track a product view"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        if 'product_id' not in data:
            return format_error_response("Product ID is required")
        
        product_id = data['product_id']
        view_duration = data.get('view_duration', 0)
        
        # Check if product exists
        product = Product.objects(id=product_id, is_active=True).first()
        if not product:
            return format_error_response("Product not found", 404)
        
        # Create or update view tracking
        viewed_product = ViewedProduct(
            user_id=user.id,
            product_id=product_id,
            view_duration=view_duration
        )
        viewed_product.save()
        
        return format_success_response(viewed_product.to_dict(), "Product view tracked")
        
    except Exception as e:
        return format_error_response(f"Failed to track product view: {str(e)}", 500)

@tracking_bp.route('/users/<user_id>/history', methods=['GET'])
@jwt_required()
def get_user_history(user_id):
    """Get user's viewed products history"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own history or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        days = int(request.args.get('days', 30))  # Default to last 30 days
        
        # Calculate date range
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get viewed products with pagination
        viewed_products = ViewedProduct.objects(
            user_id=user_id,
            viewed_at__gte=start_date
        ).order_by('-viewed_at').paginate(
            page=page, per_page=per_page
        )
        
        # Get product details for each viewed product
        history_items = []
        for viewed_product in viewed_products.items:
            product = Product.objects(id=viewed_product.product_id).first()
            if product:
                item_data = viewed_product.to_dict()
                item_data['product'] = product.to_dict()
                history_items.append(item_data)
        
        return format_success_response({
            'history': history_items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': viewed_products.total,
                'pages': viewed_products.pages,
                'has_next': viewed_products.has_next,
                'has_prev': viewed_products.has_prev
            }
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get user history: {str(e)}", 500)

@tracking_bp.route('/users/<user_id>/history/recent', methods=['GET'])
@jwt_required()
def get_recent_history(user_id):
    """Get user's recent viewed products"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own history or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        limit = int(request.args.get('limit', 10))
        
        # Get recent viewed products
        viewed_products = ViewedProduct.objects(
            user_id=user_id
        ).order_by('-viewed_at').limit(limit)
        
        # Get product details for each viewed product
        recent_items = []
        for viewed_product in viewed_products:
            product = Product.objects(id=viewed_product.product_id).first()
            if product and product.is_active:
                item_data = viewed_product.to_dict()
                item_data['product'] = product.to_dict()
                recent_items.append(item_data)
        
        return format_success_response(recent_items)
        
    except Exception as e:
        return format_error_response(f"Failed to get recent history: {str(e)}", 500)

@tracking_bp.route('/users/<user_id>/history/stats', methods=['GET'])
@jwt_required()
def get_user_history_stats(user_id):
    """Get user's viewing statistics"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own stats or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        # Get total views
        total_views = ViewedProduct.objects(user_id=user_id).count()
        
        # Get views by category
        viewed_products = ViewedProduct.objects(user_id=user_id)
        category_stats = {}
        for viewed_product in viewed_products:
            product = Product.objects(id=viewed_product.product_id).first()
            if product:
                category = product.category
                if category not in category_stats:
                    category_stats[category] = 0
                category_stats[category] += 1
        
        # Get most viewed products
        most_viewed = {}
        for viewed_product in viewed_products:
            product_id = str(viewed_product.product_id)
            if product_id not in most_viewed:
                most_viewed[product_id] = {
                    'product_id': product_id,
                    'view_count': 0,
                    'total_duration': 0
                }
            most_viewed[product_id]['view_count'] += 1
            most_viewed[product_id]['total_duration'] += viewed_product.view_duration
        
        # Sort by view count
        most_viewed_list = sorted(
            most_viewed.values(),
            key=lambda x: x['view_count'],
            reverse=True
        )[:5]
        
        return format_success_response({
            'total_views': total_views,
            'category_stats': category_stats,
            'most_viewed': most_viewed_list
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get user stats: {str(e)}", 500)

