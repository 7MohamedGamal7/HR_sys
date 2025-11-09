@echo off
REM HR Management System - Quick Setup Script for Windows
REM نظام إدارة الموارد البشرية - سكريبت الإعداد السريع

echo ========================================
echo HR Management System - Quick Setup
echo نظام إدارة الموارد البشرية - الإعداد السريع
echo ========================================
echo.

REM Check if Python is installed
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo Python is installed ✓
echo.

REM Check if virtual environment exists
echo [2/7] Checking virtual environment...
if exist "venv\" (
    echo Virtual environment already exists ✓
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created ✓
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated ✓
echo.

REM Upgrade pip
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Pip upgraded ✓
echo.

REM Install requirements
echo [5/7] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)
echo Dependencies installed ✓
echo.

REM Run migrations
echo [6/7] Running database migrations...
echo.
echo IMPORTANT: Make sure SQL Server is running and configured in settings.py
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to make migrations
    echo Please check database configuration in HR_sys/settings.py
    pause
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    echo Please check database connection and try again
    pause
    exit /b 1
)
echo Migrations completed ✓
echo.

REM Collect static files
echo [7/7] Collecting static files...
python manage.py collectstatic --noinput
echo Static files collected ✓
echo.

echo ========================================
echo Setup completed successfully! ✓
echo الإعداد اكتمل بنجاح! ✓
echo ========================================
echo.
echo Next steps:
echo 1. Create superuser: python manage.py createsuperuser
echo 2. Run server: python manage.py runserver
echo 3. Access application: http://localhost:8000/
echo.
echo Press any key to exit...
pause >nul

