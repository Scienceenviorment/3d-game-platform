@echo off
REM Windows batch script to start the 3D Game Platform

echo Starting 3D Game Platform...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run the development server launcher
python run_dev.py

pause