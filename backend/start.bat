@echo off
echo Starting E-commerce Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please check the errors above.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database is populated
echo Checking if database is populated...
python -c "from app import create_app; from models import Product; app = create_app(); app.app_context().push(); print('Products in database:', Product.objects.count())" 2>nul
if errorlevel 1 (
    echo Database not populated. Running populate script...
    python populate_db.py
    if errorlevel 1 (
        echo Failed to populate database. Please check MongoDB connection.
        pause
        exit /b 1
    )
)

REM Start the Flask application
echo Starting Flask application...
echo API will be available at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause

