@echo off
cd /d "%~dp0"

if not exist "backend\venv\Scripts\activate.bat" (
    echo [ERROR] Backend dependencies not found. Please run install_deps.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not found. Please run install_deps.bat first.
    pause
    exit /b 1
)

echo [INFO] Starting servers...
start "Backend" cmd /c "cd /d "%~dp0\backend" && .\venv\Scripts\activate.bat && langgraph dev --no-browser"
start "Frontend" cmd /c "cd /d "%~dp0\frontend" && npm run dev"

timeout /t 15 >nul
start http://localhost:5173/app/