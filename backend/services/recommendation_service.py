"""Recommendation Service - Business logic for product recommendations"""
from models import Product, ViewedProduct, User
from utils import calculate_similarity_score, get_content_similarity
from typing import List, Dict
from collections import defaultdict

class RecommendationService:
    @staticmethod
    def get_content_based_recommendations(user_id: str, limit: int = 10) -> List[Dict]:
        """Get content-based recommendations"""
        viewed_products = ViewedProduct.objects(user_id=user_id).order_by('-viewed_at').limit(20)
        if not viewed_products:
            return RecommendationService._get_popular_products(limit)
        
        viewed_product_ids = [str(vp.product_id) for vp in viewed_products]
        viewed_products_data = Product.objects(id__in=viewed_product_ids, is_active=True)
        
        if not viewed_products_data:
            return RecommendationService._get_popular_products(limit)
        
        all_products = Product.objects(is_active=True)
        product_scores = []
        
        for product in all_products:
            if str(product.id) in viewed_product_ids:
                continue
            
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
        
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        return product_scores[:limit]
    
    @staticmethod
    def get_collaborative_recommendations(user_id: str, limit: int = 10) -> List[Dict]:
        """Get collaborative filtering recommendations"""
        user_viewed = ViewedProduct.objects(user_id=user_id)
        user_product_ids = [str(vp.product_id) for vp in user_viewed]
        
        if not user_product_ids:
            return RecommendationService._get_popular_products(limit)
        
        all_users = User.objects()
        similar_users = []
        
        for user in all_users:
            if str(user.id) == user_id:
                continue
            
            other_viewed = ViewedProduct.objects(user_id=user.id)
            other_product_ids = [str(vp.product_id) for vp in other_viewed]
            
            if other_product_ids:
                similarity = calculate_similarity_score(user_product_ids, other_product_ids)
                if similarity > 0.1:
                    similar_users.append({
                        'user_id': str(user.id),
                        'similarity': similarity,
                        'viewed_products': other_product_ids
                    })
        
        if not similar_users:
            return RecommendationService._get_popular_products(limit)
        
        similar_users.sort(key=lambda x: x['similarity'], reverse=True)
        
        recommended_products = defaultdict(float)
        
        for similar_user in similar_users[:10]:
            for product_id in similar_user['viewed_products']:
                if product_id not in user_product_ids:
                    recommended_products[product_id] += similar_user['similarity']
        
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
        
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        return product_scores[:limit]
    
    @staticmethod
    def get_hybrid_recommendations(user_id: str, limit: int = 10) -> List[Dict]:
        """Get hybrid recommendations combining content-based and collaborative"""
        content_recs = RecommendationService.get_content_based_recommendations(user_id, limit)
        collab_recs = RecommendationService.get_collaborative_recommendations(user_id, limit)
        
        recommendations = content_recs + collab_recs
        
        seen_products = set()
        unique_recommendations = []
        
        for rec in recommendations:
            product_id = rec['product_id']
            if product_id not in seen_products:
                seen_products.add(product_id)
                unique_recommendations.append(rec)
                if len(unique_recommendations) >= limit:
                    break
        
        return unique_recommendations
    
    @staticmethod
    def _get_popular_products(limit: int) -> List[Dict]:
        """Get popular products as fallback"""
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
