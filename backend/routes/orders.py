from flask import Blueprint, request, jsonify
from models import Order, OrderItem, Cart, Product, User
from utils import get_current_user, format_error_response, format_success_response, validate_required_fields
from flask_jwt_extended import jwt_required
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order from cart"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        required_fields = ['shipping_address', 'payment_method']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return format_error_response(message)
        
        # Get user's cart
        cart = Cart.objects(user_id=user.id).first()
        if not cart or not cart.items:
            return format_error_response("Cart is empty", 400)
        
        # Validate cart items and calculate total
        order_items = []
        total_amount = 0.0
        
        for cart_item in cart.items:
            product = Product.objects(id=cart_item.product_id, is_active=True).first()
            if not product:
                return format_error_response(f"Product {cart_item.product_id} not found", 404)
            
            if product.stock_quantity < cart_item.quantity:
                return format_error_response(f"Insufficient stock for {product.name}", 400)
            
            # Create order item
            order_item = OrderItem(
                product_id=cart_item.product_id,
                product_name=product.name,
                quantity=cart_item.quantity,
                price=product.price
            )
            order_items.append(order_item)
            total_amount += product.price * cart_item.quantity
        
        # Create order
        order = Order(
            user_id=user.id,
            items=order_items,
            total_amount=round(total_amount, 2),
            shipping_address=data['shipping_address'],
            payment_method=data['payment_method']
        )
        order.save()
        
        # Update product stock
        for cart_item in cart.items:
            product = Product.objects(id=cart_item.product_id).first()
            if product:
                product.stock_quantity -= cart_item.quantity
                product.save()
        
        # Clear cart
        cart.items = []
        cart.save()
        
        return format_success_response(order.to_dict(), "Order created successfully", 201)
        
    except Exception as e:
        return format_error_response(f"Failed to create order: {str(e)}", 500)

@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        status = request.args.get('status')
        
        # Build query
        query = {'user_id': user.id}
        if status:
            query['status'] = status
        
        # Get orders with pagination
        orders = Order.objects(**query).order_by('-created_at').paginate(
            page=page, per_page=per_page
        )
        
        orders_data = [order.to_dict() for order in orders.items]
        
        return format_success_response({
            'orders': orders_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'pages': orders.pages,
                'has_next': orders.has_next,
                'has_prev': orders.has_prev
            }
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get orders: {str(e)}", 500)

@orders_bp.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get specific order details"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        order = Order.objects(id=order_id, user_id=user.id).first()
        if not order:
            return format_error_response("Order not found", 404)
        
        return format_success_response(order.to_dict())
        
    except Exception as e:
        return format_error_response(f"Failed to get order: {str(e)}", 500)

@orders_bp.route('/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (for admin or user cancellation)"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        if 'status' not in data:
            return format_error_response("Status is required")
        
        new_status = data['status']
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return format_error_response("Invalid status")
        
        order = Order.objects(id=order_id, user_id=user.id).first()
        if not order:
            return format_error_response("Order not found", 404)
        
        # Check if user can update status (only pending orders can be cancelled by user)
        if new_status == 'cancelled' and order.status != 'pending':
            return format_error_response("Only pending orders can be cancelled")
        
        order.status = new_status
        order.updated_at = datetime.utcnow()
        order.save()
        
        return format_success_response(order.to_dict(), "Order status updated")
        
    except Exception as e:
        return format_error_response(f"Failed to update order status: {str(e)}", 500)

@orders_bp.route('/users/<user_id>/orders', methods=['GET'])
@jwt_required()
def get_user_orders(user_id):
    """Get orders for a specific user (admin or own orders)"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own orders or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        status = request.args.get('status')
        
        # Build query
        query = {'user_id': user_id}
        if status:
            query['status'] = status
        
        # Get orders with pagination
        orders = Order.objects(**query).order_by('-created_at').paginate(
            page=page, per_page=per_page
        )
        
        orders_data = [order.to_dict() for order in orders.items]
        
        return format_success_response({
            'orders': orders_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'pages': orders.pages,
                'has_next': orders.has_next,
                'has_prev': orders.has_prev
            }
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get user orders: {str(e)}", 500)

