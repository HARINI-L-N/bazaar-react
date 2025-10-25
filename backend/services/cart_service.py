"""Cart Service - Business logic for shopping cart"""
from models import Cart, CartItem, Product
from datetime import datetime
from typing import Dict, Optional

class CartService:
    @staticmethod
    def get_cart(user_id: str) -> Dict:
        """Get user's cart with product details"""
        cart = Cart.objects(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            cart.save()
        
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
                cart.items.remove(item)
        
        cart.save()
        
        return {
            'items': cart_items,
            'total_amount': round(total_amount, 2),
            'item_count': len(cart_items)
        }
    
    @staticmethod
    def add_to_cart(user_id: str, product_id: str, quantity: int) -> Dict:
        """Add item to cart"""
        product = Product.objects(id=product_id, is_active=True).first()
        if not product:
            raise ValueError("Product not found")
        
        if product.stock_quantity < quantity:
            raise ValueError("Insufficient stock")
        
        cart = Cart.objects(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
        
        existing_item = None
        for item in cart.items:
            if str(item.product_id) == product_id:
                existing_item = item
                break
        
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                raise ValueError("Insufficient stock")
            existing_item.quantity = new_quantity
        else:
            cart_item = CartItem(product_id=product_id, quantity=quantity)
            cart.items.append(cart_item)
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return cart.to_dict()
    
    @staticmethod
    def update_cart_item(user_id: str, product_id: str, quantity: int) -> Dict:
        """Update cart item quantity"""
        cart = Cart.objects(user_id=user_id).first()
        if not cart:
            raise ValueError("Cart not found")
        
        item_found = False
        for item in cart.items:
            if str(item.product_id) == product_id:
                if quantity == 0:
                    cart.items.remove(item)
                else:
                    product = Product.objects(id=product_id).first()
                    if product and product.stock_quantity < quantity:
                        raise ValueError("Insufficient stock")
                    item.quantity = quantity
                item_found = True
                break
        
        if not item_found:
            raise ValueError("Item not found in cart")
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return cart.to_dict()
    
    @staticmethod
    def remove_from_cart(user_id: str, product_id: str) -> Dict:
        """Remove item from cart"""
        cart = Cart.objects(user_id=user_id).first()
        if not cart:
            raise ValueError("Cart not found")
        
        item_found = False
        for item in cart.items:
            if str(item.product_id) == product_id:
                cart.items.remove(item)
                item_found = True
                break
        
        if not item_found:
            raise ValueError("Item not found in cart")
        
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return cart.to_dict()
    
    @staticmethod
    def clear_cart(user_id: str) -> Dict:
        """Clear all items from cart"""
        cart = Cart.objects(user_id=user_id).first()
        if not cart:
            raise ValueError("Cart not found")
        
        cart.items = []
        cart.updated_at = datetime.utcnow()
        cart.save()
        
        return cart.to_dict()
