@echo off
title Ancient Bharat - Permission Setup
echo.
echo ===============================================
echo    ANCIENT BHARAT - FULL PERMISSIONS SETUP
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Setting up permissions...
echo.

REM Run the permission setup script
python setup_permissions.py

echo.
echo Setup complete! You can now run the game with:
echo   - Double-click start_game.bat
echo   - Or run: python simple_setup.py
echo.
pause