from flask import Blueprint, request, jsonify
from models import Product, ViewedProduct, User, Order, OrderItem
from utils import get_current_user, format_error_response, format_success_response, calculate_similarity_score, get_content_similarity
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from collections import defaultdict
import random

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations/<user_id>', methods=['GET'])
@jwt_required()
def get_recommendations(user_id):
    """Get product recommendations for a user using content-based and collaborative filtering"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own recommendations or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        # Get query parameters
        limit = int(request.args.get('limit', 10))
        algorithm = request.args.get('algorithm', 'hybrid')  # content, collaborative, hybrid
        
        recommendations = []
        
        if algorithm in ['content', 'hybrid']:
            content_recs = get_content_based_recommendations(user_id, limit)
            recommendations.extend(content_recs)
        
        if algorithm in ['collaborative', 'hybrid']:
            collab_recs = get_collaborative_recommendations(user_id, limit)
            recommendations.extend(collab_recs)
        
        # Remove duplicates and limit results
        seen_products = set()
        unique_recommendations = []
        
        for rec in recommendations:
            product_id = rec['product_id']
            if product_id not in seen_products:
                seen_products.add(product_id)
                unique_recommendations.append(rec)
                if len(unique_recommendations) >= limit:
                    break
        
        return format_success_response({
            'recommendations': unique_recommendations,
            'algorithm': algorithm,
            'count': len(unique_recommendations)
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get recommendations: {str(e)}", 500)

def get_content_based_recommendations(user_id, limit):
    """Get content-based recommendations"""
    try:
        # Get user's viewed products
        viewed_products = ViewedProduct.objects(user_id=user_id).order_by('-viewed_at').limit(20)
        if not viewed_products:
            # If no history, return popular products
            return get_popular_products(limit)
        
        # Get product details for viewed items
        viewed_product_ids = [str(vp.product_id) for vp in viewed_products]
        viewed_products_data = Product.objects(id__in=viewed_product_ids, is_active=True)
        
        if not viewed_products_data:
            return get_popular_products(limit)
        
        # Calculate similarity scores for all products
        all_products = Product.objects(is_active=True)
        product_scores = []
        
        for product in all_products:
            if str(product.id) in viewed_product_ids:
                continue  # Skip already viewed products
            
            max_similarity = 0.0
            for viewed_product in viewed_products_data:
                similarity = get_content_similarity(product, viewed_product)
                max_similarity = max(max_similarity, similarity)
            
            if max_similarity > 0:
                product_scores.append({
                    'product_id': str(product.id),
                    'product': product.to_dict(),
                    'score': max_similarity,
                    'algorithm': 'content_based'
                })
        
        # Sort by similarity score
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return product_scores[:limit]
        
    except Exception as e:
        print(f"Error in content-based recommendations: {e}")
        return get_popular_products(limit)

def get_collaborative_recommendations(user_id, limit):
    """Get collaborative filtering recommendations"""
    try:
        # Get user's viewed products
        user_viewed = ViewedProduct.objects(user_id=user_id)
        user_product_ids = [str(vp.product_id) for vp in user_viewed]
        
        if not user_product_ids:
            return get_popular_products(limit)
        
        # Find similar users based on viewed products
        all_users = User.objects()
        similar_users = []
        
        for user in all_users:
            if str(user.id) == user_id:
                continue  # Skip current user
            
            other_viewed = ViewedProduct.objects(user_id=user.id)
            other_product_ids = [str(vp.product_id) for vp in other_viewed]
            
            if other_product_ids:
                similarity = calculate_similarity_score(user_product_ids, other_product_ids)
                if similarity > 0.1:  # Minimum similarity threshold
                    similar_users.append({
                        'user_id': str(user.id),
                        'similarity': similarity,
                        'viewed_products': other_product_ids
                    })
        
        if not similar_users:
            return get_popular_products(limit)
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Get products viewed by similar users
        recommended_products = defaultdict(float)
        
        for similar_user in similar_users[:10]:  # Top 10 similar users
            for product_id in similar_user['viewed_products']:
                if product_id not in user_product_ids:
                    recommended_products[product_id] += similar_user['similarity']
        
        # Get product details and calculate final scores
        product_scores = []
        for product_id, score in recommended_products.items():
            product = Product.objects(id=product_id, is_active=True).first()
            if product:
                product_scores.append({
                    'product_id': product_id,
                    'product': product.to_dict(),
                    'score': score,
                    'algorithm': 'collaborative'
                })
        
        # Sort by score
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return product_scores[:limit]
        
    except Exception as e:
        print(f"Error in collaborative recommendations: {e}")
        return get_popular_products(limit)

def get_popular_products(limit):
    """Get popular products as fallback recommendations"""
    try:
        products = Product.objects(
            is_active=True,
            rating__gte=3.0
        ).order_by('-rating', '-review_count').limit(limit)
        
        recommendations = []
        for product in products:
            recommendations.append({
                'product_id': str(product.id),
                'product': product.to_dict(),
                'score': product.rating,
                'algorithm': 'popular'
            })
        
        return recommendations
        
    except Exception as e:
        print(f"Error getting popular products: {e}")
        return []

@recommendations_bp.route('/recommendations/<user_id>/similar/<product_id>', methods=['GET'])
@jwt_required()
def get_similar_products(user_id, product_id):
    """Get products similar to a specific product"""
    try:
        current_user = get_current_user()
        if not current_user:
            return format_error_response("User not found", 404)
        
        # Check if user is requesting their own recommendations or is admin
        if str(current_user.id) != user_id and current_user.username != 'admin':
            return format_error_response("Access denied", 403)
        
        limit = int(request.args.get('limit', 8))
        
        # Get the reference product
        reference_product = Product.objects(id=product_id, is_active=True).first()
        if not reference_product:
            return format_error_response("Product not found", 404)
        
        # Find similar products
        all_products = Product.objects(is_active=True)
        similar_products = []
        
        for product in all_products:
            if str(product.id) == product_id:
                continue  # Skip the reference product
            
            similarity = get_content_similarity(reference_product, product)
            if similarity > 0.1:  # Minimum similarity threshold
                similar_products.append({
                    'product_id': str(product.id),
                    'product': product.to_dict(),
                    'similarity': similarity
                })
        
        # Sort by similarity
        similar_products.sort(key=lambda x: x['similarity'], reverse=True)
        
        return format_success_response({
            'reference_product': reference_product.to_dict(),
            'similar_products': similar_products[:limit],
            'count': len(similar_products[:limit])
        })
        
    except Exception as e:
        return format_error_response(f"Failed to get similar products: {str(e)}", 500)

