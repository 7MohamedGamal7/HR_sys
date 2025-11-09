# HR Management System

A comprehensive Human Resources Management System built with Django that provides features for managing employees, attendance, leaves, payroll, and generating reports.

## Features

- **User Authentication**: Secure login system with role-based access control
- **Dashboard**: Professional dashboard with key HR metrics and visualizations
- **Employee Management**: 
  - Add, edit, and delete employee records
  - View detailed employee information
  - Search and filter employees
- **Attendance Management**:
  - Track employee attendance
  - Import attendance data
  - Filter by date and employee
- **Leave Management**:
  - Apply for leaves
  - Approve/reject leave requests
  - Track leave balances
- **Payroll Management**:
  - Generate payslips
  - Manage salary information
  - Track loans and deductions
- **Reports**:
  - Generate various HR reports
  - Export reports to PDF/CSV
  - Visualize data with charts
- **System Settings**:
  - Configure company information
  - Set attendance policies
  - Manage leave policies
  - Configure payroll settings

## Technology Stack

- **Backend**: Django 5.2.8 (Python 3.8+)
- **Database**: Microsoft SQL Server
- **Frontend**: 
  - Bootstrap 5
  - Font Awesome
  - Chart.js
- **Authentication**: Django Authentication System

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd HR_sys
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database settings in `HR_sys/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'mssql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'your_server',
           'PORT': '1433',
           'OPTIONS': {
               'driver': 'ODBC Driver 17 for SQL Server',
           },
       }
   }
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Access the admin panel at `http://127.0.0.1:8000/admin/`
2. Access the HR system at `http://127.0.0.1:8000/`
3. Login with your superuser credentials or create regular user accounts

## Project Structure

```
HR_sys/
├── HR_sys/              # Django project settings
│   ├── __init__.py
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py
├── hr_app/              # Main HR application
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JavaScript, images
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   ├── admin.py         # Admin configuration
│   └── ...
└── manage.py            # Django management script
```

## Database Models

The system includes the following database models:

- **TblEmployees**: Employee information
- **TblAttendance**: Daily attendance records
- **TblLates**: Late arrival records
- **TblLeaves**: Leave applications
- **TblLoans**: Employee loans
- **TblLogs**: System logs
- **TblOvertime**: Overtime records
- **TblPayslips**: Payroll information
- **TblSettings**: System configuration
- **TblStagingAttendance**: Staging table for attendance data

## Security Features

- User authentication and authorization
- Password encryption
- CSRF protection
- SQL injection prevention
- Secure session management

## Customization

The system is designed to be easily customizable:

1. **Templates**: All HTML templates can be modified in the `templates/hr_app/` directory
2. **Styles**: CSS can be modified in `static/css/style.css`
3. **Scripts**: JavaScript can be modified in `static/js/script.js`
4. **Models**: Database models can be extended in `models.py`
5. **Views**: Business logic can be modified in `views.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact the development team or create an issue in the repository.