# Backend Architecture

## 📁 Project Structure

```
backend/
├── app.py                    # Main Flask application
├── models.py                 # MongoDB models and schemas
├── utils.py                  # Utility functions and helpers
├── requirements.txt          # Python dependencies
├── populate_db.py           # Database seeding script
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_products.py
│   └── test_auth.py
├── seeds/                   # Seed data files
│   ├── __init__.py
│   ├── user_seeds.py
│   └── product_seeds.py
├── services/                # Business logic layer
│   ├── __init__.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── recommendation_service.py
└── routes/                  # API route handlers
    ├── __init__.py
    ├── auth.py
    ├── products.py
    ├── cart.py
    ├── orders.py
    ├── tracking.py
    └── recommendations.py
```

## 🏗️ Architecture Layers

### 1. Routes Layer (`routes/`)
- **Purpose**: Handle HTTP requests and responses
- **Responsibility**: 
  - Request validation
  - Authentication checks
  - Response formatting
  - Error handling

### 2. Services Layer (`services/`)
- **Purpose**: Business logic and data processing
- **Responsibility**:
  - Complex business rules
  - Data transformations
  - Algorithm implementations
  - Cross-model operations

### 3. Models Layer (`models.py`)
- **Purpose**: Database schema and ORM definitions
- **Responsibility**:
  - Data models
  - Database operations
  - Validation

### 4. Utilities Layer (`utils.py`)
- **Purpose**: Shared helper functions
- **Responsibility**:
  - Common functions
  - Helper methods
  - Utilities

## 🔄 Request Flow

```
Client Request
    ↓
Routes (auth, validation)
    ↓
Services (business logic)
    ↓
Models (database operations)
    ↓
Response to Client
```

## 📊 Service Details

### ProductService
- `get_all_products()` - Get paginated products with filters
- `get_product_by_id()` - Get single product
- `get_categories()` - Get all categories
- `get_featured_products()` - Get top-rated products
- `get_similar_products()` - Content-based recommendations

### CartService
- `get_cart()` - Get user's cart with product details
- `add_to_cart()` - Add item to cart
- `update_cart_item()` - Update item quantity
- `remove_from_cart()` - Remove item from cart
- `clear_cart()` - Clear all items

### RecommendationService
- `get_content_based_recommendations()` - Product similarity algorithm
- `get_collaborative_recommendations()` - User similarity algorithm
- `get_hybrid_recommendations()` - Combined approach
- `_get_popular_products()` - Fallback recommendations

## 🧪 Testing

### Test Structure
- `tests/test_products.py` - Product API tests
- `tests/test_auth.py` - Authentication tests

### Running Tests
```bash
python -m pytest tests/
```

## 🌱 Seeds

### Seed Data
- `seeds/user_seeds.py` - Sample users
- `seeds/product_seeds.py` - Sample products

### Populating Database
```bash
python populate_db.py
```

## 🔐 Security

- JWT authentication for protected routes
- Password hashing with Werkzeug
- CORS configuration
- Input validation
- Error handling

## 📝 Best Practices

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **DRY Principle**: Services contain reusable business logic
3. **Testability**: Services can be tested independently
4. **Maintainability**: Clear structure for easy updates
5. **Scalability**: Modular design supports growth
