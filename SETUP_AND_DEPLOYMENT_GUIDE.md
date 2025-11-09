# 🚀 HR Management System - Setup and Deployment Guide

## دليل التثبيت والنشر لنظام إدارة الموارد البشرية

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Database Configuration](#database-configuration)
4. [Running Migrations](#running-migrations)
5. [Creating Superuser](#creating-superuser)
6. [Running the Development Server](#running-the-development-server)
7. [Setting up Celery](#setting-up-celery)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Software:
- **Python 3.8+** (Recommended: Python 3.10 or 3.11)
- **Microsoft SQL Server** (2016 or later)
- **ODBC Driver 17 for SQL Server**
- **Redis Server** (for Celery background tasks)
- **Git** (for version control)

### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

### Check if pip is installed:
```bash
pip --version
# or
python -m pip --version
```

---

## 2. Installation Steps

### Step 1: Create Virtual Environment

**On Windows:**
```bash
# Navigate to project directory
cd E:\My_Project\Django_Project\HR_sys\HR_sys

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
# Navigate to project directory
cd /path/to/HR_sys

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 3: Install ODBC Driver (if not installed)

**On Windows:**
- Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Install "ODBC Driver 17 for SQL Server"

**On Linux (Ubuntu/Debian):**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

---

## 3. Database Configuration

### Step 1: Create Database in SQL Server

```sql
-- Connect to SQL Server Management Studio (SSMS)
-- Run the following SQL commands:

CREATE DATABASE HR_System;
GO

-- Create a login for the application
CREATE LOGIN hr_admin WITH PASSWORD = 'YourStrongPassword123!';
GO

-- Create a user in the database
USE HR_System;
GO

CREATE USER hr_admin FOR LOGIN hr_admin;
GO

-- Grant permissions
ALTER ROLE db_owner ADD MEMBER hr_admin;
GO
```

### Step 2: Update Django Settings

Edit `HR_sys/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'HR_System',  # Your database name
        'USER': 'hr_admin',   # Your SQL Server username
        'PASSWORD': 'YourStrongPassword123!',  # Your password
        'HOST': '192.168.1.48',  # Your SQL Server IP or 'localhost'
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

### Step 3: Test Database Connection

```bash
python manage.py dbshell
```

If successful, you'll see the SQL Server prompt.

---

## 4. Running Migrations

### Step 1: Make Migrations

```bash
python manage.py makemigrations
```

Expected output:
```
Migrations for 'core':
  core/migrations/0001_initial.py
    - Create model User
    - Create model Notification
    ...
Migrations for 'employees':
  employees/migrations/0001_initial.py
    - Create model Employee
    ...
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, employees, attendance, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 3: Verify Tables Created

```bash
python manage.py dbshell
```

Then run:
```sql
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';
```

---

## 5. Creating Superuser

### Create Admin Account

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- **Username**: admin (or your preferred username)
- **Email**: admin@example.com
- **Password**: (enter a strong password)
- **Password (again)**: (confirm password)

---

## 6. Running the Development Server

### Step 1: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 2: Start Development Server

```bash
python manage.py runserver
```

Or specify a custom port:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Step 3: Access the Application

Open your browser and navigate to:
- **Application**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Login**: http://localhost:8000/login/

---

## 7. Setting up Celery

### Step 1: Install Redis

**On Windows:**
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Or use WSL (Windows Subsystem for Linux)

**On Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Step 2: Test Redis Connection

```bash
redis-cli ping
```

Expected output: `PONG`

### Step 3: Start Celery Worker

**In a new terminal (with virtual environment activated):**

```bash
# On Windows
celery -A HR_sys worker -l info --pool=solo

# On Linux/Mac
celery -A HR_sys worker -l info
```

### Step 4: Start Celery Beat (for scheduled tasks)

**In another terminal:**

```bash
# On Windows
celery -A HR_sys beat -l info

# On Linux/Mac
celery -A HR_sys beat -l info
```

---

## 8. Production Deployment

### Option 1: Deploy with Gunicorn + Nginx (Linux)

#### Step 1: Install Gunicorn

```bash
pip install gunicorn
```

#### Step 2: Create Gunicorn Service

Create `/etc/systemd/system/hr_system.service`:

```ini
[Unit]
Description=HR System Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/HR_sys
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/path/to/HR_sys/hr_system.sock HR_sys.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Step 3: Configure Nginx

Create `/etc/nginx/sites-available/hr_system`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/HR_sys;
    }
    
    location /media/ {
        root /path/to/HR_sys;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/HR_sys/hr_system.sock;
    }
}
```

#### Step 4: Enable and Start Services

```bash
sudo systemctl start hr_system
sudo systemctl enable hr_system
sudo systemctl restart nginx
```

### Option 2: Deploy with IIS (Windows)

#### Step 1: Install wfastcgi

```bash
pip install wfastcgi
wfastcgi-enable
```

#### Step 2: Configure IIS

1. Open IIS Manager
2. Add new website
3. Set physical path to project directory
4. Configure FastCGI settings
5. Add web.config file

---

## 9. Troubleshooting

### Issue 1: "No module named 'django'"

**Solution:**
```bash
# Make sure virtual environment is activated
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

# Then install requirements
pip install -r requirements.txt
```

### Issue 2: "ODBC Driver not found"

**Solution:**
- Install ODBC Driver 17 for SQL Server
- Update driver name in settings.py if using different version

### Issue 3: "Cannot connect to database"

**Solution:**
- Check SQL Server is running
- Verify firewall allows connection on port 1433
- Test connection with SQL Server Management Studio
- Verify credentials in settings.py

### Issue 4: "Static files not loading"

**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue 5: "Celery not working"

**Solution:**
- Ensure Redis is running: `redis-cli ping`
- Check Celery worker is running
- Check Celery beat is running for scheduled tasks

---

## 📝 Quick Start Commands

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database in settings.py

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Run development server
python manage.py runserver

# 8. (Optional) Start Celery worker
celery -A HR_sys worker -l info --pool=solo

# 9. (Optional) Start Celery beat
celery -A HR_sys beat -l info
```

---

## 🔐 Security Checklist for Production

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Configure CSRF and CORS settings
- [ ] Set up regular database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Use strong passwords for database and admin

---

## 📞 Support

For issues or questions:
- Check the documentation
- Review error logs in `logs/` directory
- Contact system administrator

---

**Last Updated**: 2025-11-09
**Version**: 1.0.0

