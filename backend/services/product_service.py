"""Product Service - Business logic for products"""
from models import Product
from utils import get_content_similarity
from typing import List, Dict, Optional

class ProductService:
    @staticmethod
    def get_all_products(page=1, per_page=10, filters=None):
        """Get all products with pagination and filtering"""
        query = {'is_active': True}
        
        if filters:
            if filters.get('category'):
                query['category'] = filters['category']
            if filters.get('search'):
                query['$or'] = [
                    {'name': {'$regex': filters['search'], '$options': 'i'}},
                    {'description': {'$regex': filters['search'], '$options': 'i'}}
                ]
            if filters.get('min_price'):
                query['price'] = {'$gte': float(filters['min_price'])}
            if filters.get('max_price'):
                if 'price' in query:
                    query['price']['$lte'] = float(filters['max_price'])
                else:
                    query['price'] = {'$lte': float(filters['max_price'])}
        
        sort_by = filters.get('sort_by', 'created_at') if filters else 'created_at'
        sort_order = filters.get('sort_order', 'desc') if filters else 'desc'
        
        sort_criteria = [('created_at', -1 if sort_order == 'desc' else 1)]
        if sort_by == 'price':
            sort_criteria = [('price', 1 if sort_order == 'asc' else -1)]
        elif sort_by == 'rating':
            sort_criteria = [('rating', -1 if sort_order == 'desc' else 1)]
        
        products = Product.objects(**query).order_by(*sort_criteria).paginate(
            page=page, per_page=per_page
        )
        
        return {
            'products': [product.to_dict() for product in products.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages,
                'has_next': products.has_next,
                'has_prev': products.has_prev
            }
        }
    
    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        product = Product.objects(id=product_id, is_active=True).first()
        return product.to_dict() if product else None
    
    @staticmethod
    def get_categories() -> List[str]:
        """Get all product categories"""
        return Product.objects(is_active=True).distinct('category')
    
    @staticmethod
    def get_featured_products(limit=8) -> List[Dict]:
        """Get featured products"""
        products = Product.objects(
            is_active=True,
            rating__gte=4.0
        ).order_by('-rating', '-review_count').limit(limit)
        
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_similar_products(product_id: str, limit=8) -> List[Dict]:
        """Get products similar to a given product"""
        reference_product = Product.objects(id=product_id, is_active=True).first()
        if not reference_product:
            return []
        
        all_products = Product.objects(is_active=True)
        similar_products = []
        
        for product in all_products:
            if str(product.id) == product_id:
                continue
            
            similarity = get_content_similarity(reference_product, product)
            if similarity > 0.1:
                similar_products.append({
                    'product_id': str(product.id),
                    'product': product.to_dict(),
                    'similarity': similarity
                })
        
        similar_products.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_products[:limit]
