#!/bin/bash
# HR Management System - Quick Setup Script for Linux/Mac
# نظام إدارة الموارد البشرية - سكريبت الإعداد السريع

echo "========================================"
echo "HR Management System - Quick Setup"
echo "نظام إدارة الموارد البشرية - الإعداد السريع"
echo "========================================"
echo ""

# Check if Python is installed
echo "[1/7] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi
echo "Python is installed ✓"
echo ""

# Check if virtual environment exists
echo "[2/7] Checking virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists ✓"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created ✓"
fi
echo ""

# Activate virtual environment
echo "[3/7] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "Virtual environment activated ✓"
echo ""

# Upgrade pip
echo "[4/7] Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "Pip upgraded ✓"
echo ""

# Install requirements
echo "[5/7] Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Please check requirements.txt and try again"
    exit 1
fi
echo "Dependencies installed ✓"
echo ""

# Run migrations
echo "[6/7] Running database migrations..."
echo ""
echo "IMPORTANT: Make sure SQL Server is running and configured in settings.py"
read -p "Press Enter to continue or Ctrl+C to cancel..."

python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to make migrations"
    echo "Please check database configuration in HR_sys/settings.py"
    exit 1
fi

python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to apply migrations"
    echo "Please check database connection and try again"
    exit 1
fi
echo "Migrations completed ✓"
echo ""

# Collect static files
echo "[7/7] Collecting static files..."
python manage.py collectstatic --noinput
echo "Static files collected ✓"
echo ""

echo "========================================"
echo "Setup completed successfully! ✓"
echo "الإعداد اكتمل بنجاح! ✓"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Run server: python manage.py runserver"
echo "3. Access application: http://localhost:8000/"
echo ""

