@echo off
cd /d "%~dp0"

echo.
echo =================================================================
echo  Installing Dependencies
echo =================================================================
echo.

REM 1. Create and install backend dependencies
if not exist "backend\venv\Scripts\activate.bat" (
    echo [INFO] Creating backend virtual environment...
    py -3.11 -m venv backend\venv
    if errorlevel 1 (
        echo [ERROR] Failed to create backend virtual environment.
        pause
        exit /b 1
    )
)
echo [INFO] Installing backend dependencies...
call backend\venv\Scripts\activate.bat
pip install -e backend
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies.
    pause
    exit /b 1
)

REM 2. Install frontend dependencies
if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    pushd frontend
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies.
        popd
        pause
        exit /b 1
    )
    popd
)

echo.
echo =================================================================
echo  Dependency installation complete.
echo =================================================================
echo.
pause
