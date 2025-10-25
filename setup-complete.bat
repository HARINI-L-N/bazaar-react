@echo off
echo ========================================
echo  E-commerce Full Stack Setup Script
echo ========================================
echo.

REM Check if MongoDB is installed
echo [1/4] Checking MongoDB installation...
where mongod >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: MongoDB not found in PATH.
    echo Please install MongoDB or use MongoDB Atlas (cloud)
    echo Download from: https://www.mongodb.com/try/download/community
    echo.
    pause
) else (
    echo MongoDB found!
)

REM Setup Backend
echo.
echo [2/4] Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env file with your MongoDB connection string
    echo For local MongoDB: MONGODB_URI=mongodb://localhost:27017/ecommerce_db
    echo For MongoDB Atlas: MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db
    echo.
    pause
)

echo Populating database with sample data...
python populate_db.py

cd ..

REM Setup Frontend
echo.
echo [3/4] Setting up frontend...
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

if not exist ".env" (
    echo Creating frontend .env file...
    echo VITE_API_BASE_URL=http://localhost:5000/api > .env
)

REM Display success message
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend server: cd backend ^&^& .\venv\Scripts\activate ^&^& python app.py
echo 2. Start frontend server: npm run dev
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:5173
echo.
echo Test credentials:
echo - john@example.com / password123
echo - jane@example.com / password123
echo - admin@example.com / admin123
echo.
pause
