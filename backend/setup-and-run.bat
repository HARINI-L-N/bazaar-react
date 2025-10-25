@echo off
echo ============================================
echo   E-commerce Backend Setup and Run
echo ============================================
echo.

REM Navigate to backend directory
cd /d "%~dp0"

REM Activate virtual environment
echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/4] Installing dependencies...
pip install Flask Flask-MongoEngine Flask-JWT-Extended Flask-CORS python-dotenv Werkzeug

REM Create .env file if not exists
echo [3/4] Setting up environment...
if not exist ".env" (
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your MongoDB connection
    echo Default: MONGODB_URI=mongodb://localhost:27017/ecommerce_db
    echo.
    pause
)

REM Populate database
echo [4/4] Populating database...
python populate_db.py

REM Start server
echo.
echo ============================================
echo   Starting Backend Server
echo ============================================
echo.
echo Backend running on: http://localhost:5000
echo API available at: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
