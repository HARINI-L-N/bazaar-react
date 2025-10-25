# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Prerequisites
- Python 3.8+ installed
- MongoDB running (local or cloud)
- Git (optional)

### 2. Setup (Choose your method)

#### Option A: Automated Setup (Recommended)
```bash
# Windows
python setup.py

# macOS/Linux
python3 setup.py
```

#### Option B: Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy env.example .env  # Windows
cp env.example .env   # macOS/Linux

# Populate database
python populate_db.py
```

### 3. Start the Server

#### Option A: Using startup scripts
```bash
# Windows
start.bat

# macOS/Linux
./start.sh
```

#### Option B: Manual start
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start Flask app
python app.py
```

## 🧪 Test the API

1. **Health Check**: Visit http://localhost:5000/api/health
2. **Get Products**: Visit http://localhost:5000/api/products
3. **Run Test Script**: `python test_api.py`

## 🔑 Test Credentials

- **John Doe**: john@example.com / password123
- **Jane Smith**: jane@example.com / password123  
- **Admin**: admin@example.com / admin123

## 📱 Connect with React Frontend

Update your React app's API base URL to:
```
http://localhost:5000/api
```

## 🛠️ Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod`
- Check connection string in `.env` file
- Default: `mongodb://localhost:27017/ecommerce_db`

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

### Virtual Environment Issues
- Delete `venv` folder and run setup again
- Ensure Python 3.8+ is installed

## 📚 Full Documentation

See `README.md` for complete API documentation and advanced configuration.

