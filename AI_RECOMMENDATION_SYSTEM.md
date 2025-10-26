# 🤖 AI E-Commerce Recommendation System

## 🎯 Overview

This project implements a comprehensive AI-powered e-commerce recommendation system with both **Content-Based** and **Collaborative Filtering** algorithms, built with React frontend and Flask backend.

## 🏗️ Architecture

### Backend (Flask + MongoDB)
- **Content-Based Filtering**: Uses TF-IDF vectorization and cosine similarity
- **Collaborative Filtering**: User-user similarity with Jaccard coefficient
- **Product View Tracking**: Real-time user behavior analytics
- **Smart Recommendations**: Hybrid approach combining both algorithms

### Frontend (React + Tailwind)
- **Amazon-inspired Design**: Dark theme with yellow accents
- **Context API**: Global state management for authentication
- **React Router**: Multi-page navigation
- **Real-time Integration**: Live API calls for recommendations

## 🚀 Features Implemented

### ✅ Backend Enhancements

#### 1. Advanced Content-Based Filtering
- **Endpoint**: `/api/recommendations/content/<product_id>`
- **Algorithm**: TF-IDF vectorization + cosine similarity
- **Features**: Product name, description, category, tags, features
- **Output**: 4-6 most similar products

#### 2. Collaborative Filtering
- **Endpoint**: `/api/recommendations/collaborative/<user_id>`
- **Algorithm**: User-user similarity with Jaccard coefficient
- **Data**: User viewing history and purchase patterns
- **Output**: 8-10 personalized recommendations

#### 3. Product View Tracking
- **Endpoint**: `/api/track/view`
- **Features**: View duration, duplicate prevention, real-time tracking
- **Analytics**: User behavior insights for recommendations

#### 4. Enhanced Models
- **ViewedProduct**: Tracks user interactions
- **User Preferences**: Implicit feedback collection
- **Product Metadata**: Rich feature vectors

### ✅ Frontend Implementation

#### 1. React Router Setup
- **Home** (`/`): Featured products + AI recommendations
- **Product Details** (`/products/:id`): Product info + related items
- **Login/Register** (`/login`, `/register`): Authentication
- **Profile** (`/profile`): User info + viewing history
- **Cart** (`/cart`): Shopping cart management
- **Orders** (`/orders`): Order history

#### 2. Context API Authentication
- **AuthContext**: Global authentication state
- **JWT Tokens**: Secure API communication
- **Protected Routes**: Route-level access control
- **Persistent Login**: localStorage integration

#### 3. AI Recommendation Components
- **Home Page**: "Recommendations for You" section
- **Product Details**: "Products Related to this Item"
- **Profile Page**: Recently viewed products
- **Real-time Updates**: Live recommendation fetching

#### 4. Amazon-Inspired Design
- **Color Scheme**: Dark navbar, yellow accents
- **Typography**: Clean, modern fonts
- **Responsive**: Mobile-first design
- **Icons**: Lucide React icon library
- **Animations**: Smooth transitions and hover effects

## 🧠 AI Algorithms

### Content-Based Filtering
```python
# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform(product_texts)

# Cosine Similarity
similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
```

### Collaborative Filtering
```python
# Jaccard Similarity
def calculate_similarity_score(user1_items, user2_items):
    intersection = len(set(user1_items).intersection(set(user2_items)))
    union = len(set(user1_items).union(set(user2_items)))
    return intersection / union if union > 0 else 0.0
```

## 📊 API Endpoints

### Authentication
- `POST /api/users/login` - User login
- `POST /api/users/register` - User registration

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product details

### AI Recommendations
- `GET /api/recommendations/content/:product_id` - Content-based recommendations
- `GET /api/recommendations/collaborative/:user_id` - Collaborative recommendations

### Tracking
- `POST /api/track/view` - Track product view
- `GET /api/users/:user_id/history` - User viewing history

### Cart & Orders
- `GET /api/cart` - Get user cart
- `POST /api/cart` - Add to cart
- `GET /api/orders` - Get user orders

## 🎨 Frontend Components

### Core Components
- **Navbar**: Amazon-inspired navigation with authentication
- **ProductCard**: Responsive product display with ratings
- **ProtectedRoute**: Authentication-based route protection

### Pages
- **HomePage**: Featured products + AI recommendations
- **ProductDetailPage**: Product info + related items + view tracking
- **LoginPage/RegisterPage**: Authentication forms
- **ProfilePage**: User info + viewing history
- **CartPage**: Shopping cart management
- **OrdersPage**: Order history display

## 🚀 Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python populate_db.py
python app.py
```

### 2. Frontend Setup
```bash
npm install
npm run dev
```

### 3. Test AI System
```bash
python test-ai-recommendations.py
```

## 🧪 Testing the AI System

### Manual Testing
1. **Open Frontend**: http://localhost:5173/
2. **Login**: Use test credentials (john@example.com / password123)
3. **Browse Products**: View different products to build history
4. **Check Recommendations**: See "Recommendations for You" on home page
5. **View Product Details**: See "Products Related to this Item"

### API Testing
```bash
# Test content-based recommendations
curl http://localhost:5000/api/recommendations/content/PRODUCT_ID

# Test collaborative recommendations
curl -H "Authorization: Bearer TOKEN" \
     http://localhost:5000/api/recommendations/collaborative/USER_ID
```

## 📈 Performance Features

### Smart Caching
- **View Tracking**: Prevents duplicate entries
- **Recommendation Caching**: Reduces computation time
- **User Session**: Persistent authentication

### Scalability
- **Modular Architecture**: Services layer separation
- **Database Optimization**: Indexed queries
- **API Rate Limiting**: Prevents abuse

## 🎯 Business Value

### For Users
- **Personalized Experience**: AI-driven product suggestions
- **Discovery**: Find products they might like
- **Engagement**: Increased time on site
- **Conversion**: Higher purchase rates

### For Business
- **Analytics**: User behavior insights
- **Inventory**: Popular product identification
- **Marketing**: Targeted recommendations
- **Revenue**: Increased sales through personalization

## 🔧 Customization

### Adding New Algorithms
1. **Create Service**: Add to `services/recommendation_service.py`
2. **Add Endpoint**: Create new route in `routes/recommendations.py`
3. **Frontend Integration**: Update React components

### Styling Customization
- **Colors**: Update Tailwind classes in components
- **Layout**: Modify grid systems and spacing
- **Components**: Customize ProductCard, Navbar, etc.

## 📚 Documentation

- **Backend**: `backend/ARCHITECTURE.md`
- **Setup**: `SETUP_GUIDE.md`
- **Testing**: `TESTING_GUIDE.md`
- **API**: Backend route documentation

## 🎉 Success Metrics

### Technical
- ✅ Content-based filtering working
- ✅ Collaborative filtering working
- ✅ Product view tracking active
- ✅ Real-time recommendations
- ✅ Responsive design
- ✅ Authentication system

### User Experience
- ✅ Amazon-inspired design
- ✅ Smooth navigation
- ✅ Mobile responsive
- ✅ Fast loading
- ✅ Intuitive interface

## 🚀 Next Steps

1. **A/B Testing**: Compare recommendation algorithms
2. **Machine Learning**: Implement more advanced ML models
3. **Real-time Analytics**: User behavior dashboards
4. **Mobile App**: React Native implementation
5. **Deployment**: Production deployment with Docker

---

**Your AI-powered e-commerce recommendation system is now complete!** 🎉

The system provides personalized product recommendations using state-of-the-art algorithms, creating an Amazon-like shopping experience with intelligent product suggestions.
