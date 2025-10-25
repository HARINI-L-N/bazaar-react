from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from routes.recommendations import recommendations_bp
from routes.tracking import tracking_bp

# Import models to ensure they're registered
import models

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # --- MONGODB ATLAS CONFIGURATION START ---
    
    mongo_uri = os.getenv('MONGODB_URI')
    print(f"\n--- DEBUG: MONGODB_URI LOADED: {mongo_uri} ---")
    
    if not mongo_uri:
        # If running populator script and URI is missing, raise clear error
        if os.environ.get('FLASK_ENV') != 'development': # Check if we're not running a server, but a script
             raise ValueError("MONGODB_URI is not set! Please check your .env file and path.")
        
    # Set MONGODB_HOST to ensure Flask-MongoEngine uses the full Atlas URI
    app.config['MONGODB_HOST'] = mongo_uri 
    
    # Extract database name explicitly for robust initialization
    # If URI is 'mongodb+srv://.../bazaar', db_name is 'bazaar'
    db_name = mongo_uri.split('/')[-1] if mongo_uri else 'ecommerce_db'
    
    # Use MONGODB_SETTINGS for explicit control, required for srv connections
    app.config['MONGODB_SETTINGS'] = {
        'host': mongo_uri,
        'db': db_name,
        'retryWrites': False # Helps prevent issues during initial population/testing
    }
    
    # Initialize MongoDB
    from models import db
    db.init_app(app)
    
    # --- MONGODB ATLAS CONFIGURATION END ---
    
    # Initialize extensions
    CORS(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(orders_bp, url_prefix='/api')
    app.register_blueprint(recommendations_bp, url_prefix='/api')
    app.register_blueprint(tracking_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'OK', 'message': 'E-commerce API is running'})
    
    # CRITICAL: Ensure the app object is returned!
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
