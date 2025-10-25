@echo off
echo ============================================
echo   E-commerce Status Check
echo ============================================
echo.

echo Checking Backend (Port 5000)...
netstat -an | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo ✅ Backend is running on port 5000
) else (
    echo ❌ Backend not running on port 5000
    echo    Run: cd backend ^&^& python app.py
)

echo.
echo Checking Frontend (Port 5173)...
netstat -an | findstr :5173 >nul
if %errorlevel% equ 0 (
    echo ✅ Frontend is running on port 5173
) else (
    echo ❌ Frontend not running on port 5173
    echo    Run: npm run dev
)

echo.
echo Checking MongoDB...
netstat -an | findstr :27017 >nul
if %errorlevel% equ 0 (
    echo ✅ MongoDB is running on port 27017
) else (
    echo ❌ MongoDB not running on port 27017
    echo    Install MongoDB or use MongoDB Atlas
)

echo.
echo ============================================
echo   Quick Test URLs
echo ============================================
echo.
echo Backend Health: http://localhost:5000/api/health
echo Products API:   http://localhost:5000/api/products
echo Frontend:       http://localhost:5173/
echo.
echo Test Credentials:
echo - john@example.com / password123
echo - jane@example.com / password123
echo - admin@example.com / admin123
echo.
pause
