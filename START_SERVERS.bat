@echo off
echo ========================================
echo  Starting E-commerce Servers
echo ========================================
echo.

REM Check if both directories exist
if not exist "backend" (
    echo ERROR: Backend directory not found!
    pause
    exit /b 1
)

REM Start Backend Server
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && .\venv\Scripts\activate && python app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend Server
echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ========================================
echo  Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to open browsers...
pause >nul

REM Open browsers
start http://localhost:5000/api/health
start http://localhost:5173

echo.
echo Servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
