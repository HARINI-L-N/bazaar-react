#!/bin/bash

echo "Starting E-commerce Backend..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please check the errors above."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Check if database is populated
echo "Checking if database is populated..."
python3 -c "from app import create_app; from models import Product; app = create_app(); app.app_context().push(); print('Products in database:', Product.objects.count())" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Database not populated. Running populate script..."
    python3 populate_db.py
    if [ $? -ne 0 ]; then
        echo "Failed to populate database. Please check MongoDB connection."
        exit 1
    fi
fi

# Start the Flask application
echo "Starting Flask application..."
echo "API will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo
python3 app.py

