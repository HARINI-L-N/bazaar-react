# E-commerce Backend API

A comprehensive Flask + MongoDB backend for an Amazon-inspired e-commerce web application with user authentication, product management, cart functionality, order processing, and intelligent product recommendations.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Product Management**: CRUD operations for products with categories, tags, and features
- **Shopping Cart**: Add, remove, and manage cart items
- **Order Processing**: Create and track orders with status updates
- **Product Tracking**: Track user product views for analytics and recommendations
- **Smart Recommendations**: Content-based and collaborative filtering for personalized product suggestions
- **Security**: JWT authentication, password hashing, CORS support
- **Database**: MongoDB with sample data for testing

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get JWT token
- `GET /api/users/profile` - Get current user profile
- `PUT /api/users/profile` - Update user profile

### Products
- `GET /api/products` - Get all products (with filtering and pagination)
- `GET /api/products/<id>` - Get product details
- `GET /api/products/categories` - Get all product categories
- `GET /api/products/featured` - Get featured products

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/<product_id>` - Update cart item quantity
- `DELETE /api/cart/<product_id>` - Remove item from cart
- `DELETE /api/cart/clear` - Clear all cart items

### Orders
- `POST /api/orders` - Create new order from cart
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get specific order details
- `PUT /api/orders/<id>/status` - Update order status
- `GET /api/users/<id>/orders` - Get orders for specific user

### Tracking
- `POST /api/track/view` - Track product view
- `GET /api/users/<id>/history` - Get user's viewed products history
- `GET /api/users/<id>/history/recent` - Get recent viewed products
- `GET /api/users/<id>/history/stats` - Get user viewing statistics

### Recommendations
- `GET /api/recommendations/<user_id>` - Get personalized product recommendations
- `GET /api/recommendations/<user_id>/similar/<product_id>` - Get products similar to a specific product

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- pip (Python package installer)

### Installation

1. **Clone or download the backend code**

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment variables**
   
   Copy the example environment file:
   ```bash
   copy env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-change-in-production
   JWT_SECRET_KEY=jwt-secret-string-change-in-production
   MONGODB_URI=mongodb://localhost:27017/ecommerce_db
   ```

7. **Start MongoDB**
   
   Make sure MongoDB is running on your system. If using local MongoDB:
   ```bash
   mongod
   ```

8. **Populate the database with sample data**
   ```bash
   python populate_db.py
   ```

9. **Start the Flask application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Testing the API

### Sample Users Created

The populate script creates these test users:

- **John Doe**: `john@example.com` / `password123`
- **Jane Smith**: `jane@example.com` / `password123`
- **Admin**: `admin@example.com` / `admin123`

### Sample API Calls

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:5000/api/users/register \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
   ```

2. **Login**:
   ```bash
   curl -X POST http://localhost:5000/api/users/login \
     -H "Content-Type: application/json" \
     -d '{"username": "john@example.com", "password": "password123"}'
   ```

3. **Get products** (no authentication required):
   ```bash
   curl http://localhost:5000/api/products
   ```

4. **Get recommendations** (requires authentication):
   ```bash
   curl -X GET http://localhost:5000/api/recommendations/USER_ID \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Database Schema

### Collections

- **Users**: User accounts with authentication
- **Products**: Product catalog with categories, tags, and features
- **Cart**: Shopping cart items for each user
- **Orders**: Order history and status
- **ViewedProducts**: Product view tracking for recommendations

### Sample Data

The populate script creates:
- 3 sample users
- 10 sample products across different categories
- Sample product views and interactions
- Sample cart and order data

## Recommendation System

The API implements two types of recommendation algorithms:

### Content-Based Filtering
- Analyzes product features, categories, tags, and attributes
- Recommends products similar to those the user has viewed
- Uses similarity scoring based on product characteristics

### Collaborative Filtering
- Finds users with similar viewing patterns
- Recommends products liked by similar users
- Uses Jaccard similarity to find user correlations

### Hybrid Approach
- Combines both content-based and collaborative filtering
- Provides more diverse and accurate recommendations
- Falls back to popular products for new users

## Connecting with React Frontend

To connect this backend with your React frontend:

1. **Update API base URL** in your React app to `http://localhost:5000/api`

2. **Handle authentication** by storing JWT tokens and including them in requests:
   ```javascript
   const token = localStorage.getItem('token');
   fetch('http://localhost:5000/api/products', {
     headers: {
       'Authorization': `Bearer ${token}`
     }
   });
   ```

3. **CORS is enabled** so your React app can make requests from any origin

## Production Deployment

For production deployment:

1. **Change secret keys** in environment variables
2. **Use a production MongoDB instance** (MongoDB Atlas recommended)
3. **Set up proper logging and monitoring**
4. **Use a production WSGI server** like Gunicorn
5. **Set up reverse proxy** with Nginx
6. **Enable HTTPS** for secure communication

## API Documentation

### Authentication Headers

For protected routes, include the JWT token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

### Response Format

All API responses follow this format:
```json
{
  "data": {...},
  "message": "Success message",
  "error": "Error message (if any)"
}
```

### Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**: Ensure MongoDB is running and the connection string is correct
2. **JWT Token Expired**: Tokens expire after 24 hours, re-login to get a new token
3. **CORS Issues**: CORS is enabled by default, but check if your frontend URL is allowed
4. **Port Already in Use**: Change the port in `app.py` if port 5000 is occupied

### Logs

Check the console output for detailed error messages and debugging information.

## Support

For issues or questions:
1. Check the console logs for error messages
2. Verify MongoDB is running and accessible
3. Ensure all dependencies are installed correctly
4. Check that environment variables are set properly

