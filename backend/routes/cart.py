from flask import Blueprint, request, jsonify
from models import Cart, CartItem, Product, User
from utils import get_current_user, format_error_response, format_success_response, validate_required_fields
from flask_jwt_extended import jwt_required
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        cart = Cart.objects(user_id=user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
            cart.save()
        
        # Get product details for each cart item
        cart_items = []
        total_amount = 0.0
        
        for item in cart.items:
            product = Product.objects(id=item.product_id).first()
            if product and product.is_active:
                item_data = item.to_dict()
                item_data['product'] = product.to_dict()
                item_data['subtotal'] = product.price * item.quantity
                total_amount += item_data['subtotal']
                cart_items.append(item_data)
            else:
                # Remove invalid items
                cart.items.remove(item)
        
        cart.save()
        
        return format_success_response({
            'items': cart_items,
            'total_amount': round(total_amount, 2),
            'item_count': len(cart_items)
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get cart: {str(e)}", 500)

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        required_fields = ['product_id', 'quantity']
        is_valid, message = validate_required_fields(data, required_fields)
        if not is_valid:
            return format_error_response(message)
        
        product_id = data['product_id']
        quantity = int(data['quantity'])
        
        if quantity <= 0:
            return format_error_response("Quantity must be greater than 0")
        
        # Check if product exists and is active
        product = Product.objects(id=product_id, is_active=True).first()
        if not product:
            return format_error_response("Product not found", 404)
        
        # Check stock availability
        if product.stock_quantity < quantity:
            return format_error_response("Insufficient stock")
        
        # Get or create cart
        cart = Cart.objects(user_id=user.id).first()
        if not cart:
            cart = Cart(user_id=user.id)
        
        # Check if item already exists in cart
        existing_item = None
        for item in cart.items:
            if str(item.product_id) == product_id:
                existing_item = item
                break
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return format_error_response("Insufficient stock")
            existing_item.quantity = new_quantity
        else:
            # Add new item
            cart_item = CartItem(
                product_id=product_id,
                quantity=quantity
            )
            cart.items.append(cart_item)
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return format_success_response(cart.to_dict(), "Item added to cart")
        
    except Exception as e:
        return format_error_response(f"Failed to add to cart: {str(e)}", 500)

@cart_bp.route('/cart/<product_id>', methods=['PUT'])
@jwt_required()
def update_cart_item():
    """Update cart item quantity"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        data = request.get_json()
        if 'quantity' not in data:
            return format_error_response("Quantity is required")
        
        quantity = int(data['quantity'])
        if quantity < 0:
            return format_error_response("Quantity cannot be negative")
        
        cart = Cart.objects(user_id=user.id).first()
        if not cart:
            return format_error_response("Cart not found", 404)
        
        # Find and update item
        item_found = False
        for item in cart.items:
            if str(item.product_id) == product_id:
                if quantity == 0:
                    cart.items.remove(item)
                else:
                    # Check stock availability
                    product = Product.objects(id=product_id).first()
                    if product and product.stock_quantity < quantity:
                        return format_error_response("Insufficient stock")
                    item.quantity = quantity
                item_found = True
                break
        
        if not item_found:
            return format_error_response("Item not found in cart", 404)
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return format_success_response(cart.to_dict(), "Cart updated")
        
    except Exception as e:
        return format_error_response(f"Failed to update cart: {str(e)}", 500)

@cart_bp.route('/cart/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    """Remove item from cart"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        cart = Cart.objects(user_id=user.id).first()
        if not cart:
            return format_error_response("Cart not found", 404)
        
        # Find and remove item
        item_found = False
        for item in cart.items:
            if str(item.product_id) == product_id:
                cart.items.remove(item)
                item_found = True
                break
        
        if not item_found:
            return format_error_response("Item not found in cart", 404)
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return format_success_response(cart.to_dict(), "Item removed from cart")
        
    except Exception as e:
        return format_error_response(f"Failed to remove from cart: {str(e)}", 500)

@cart_bp.route('/cart/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        user = get_current_user()
        if not user:
            return format_error_response("User not found", 404)
        
        cart = Cart.objects(user_id=user.id).first()
        if not cart:
            return format_error_response("Cart not found", 404)
        
        cart.items = []
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return format_success_response(cart.to_dict(), "Cart cleared")
        
    except Exception as e:
        return format_error_response(f"Failed to clear cart: {str(e)}", 500)

