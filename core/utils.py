"""
Utility functions for the HRMS system
"""
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import AuditLog, Notification
import logging

logger = logging.getLogger(__name__)


def log_action(user, action, model_name, object_id=None, description='', ip_address=None):
    """
    Log an action to the audit log
    تسجيل إجراء في سجل التدقيق
    
    Args:
        user: User object
        action: Action type (create, update, delete, etc.)
        model_name: Name of the model
        object_id: ID of the object
        description: Description of the action
        ip_address: IP address of the user
    """
    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            description=description,
            ip_address=ip_address
        )
    except Exception as e:
        logger.error(f"Error logging action: {e}")


def create_notification(user, title, message, notification_type='info', link=None):
    """
    Create a notification for a user
    إنشاء إشعار للمستخدم
    
    Args:
        user: User object
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, success, warning, error)
        link: Optional link
    """
    try:
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )
    except Exception as e:
        logger.error(f"Error creating notification: {e}")


def send_email_notification(subject, message, recipient_list, from_email=None):
    """
    Send email notification
    إرسال إشعار بريد إلكتروني
    
    Args:
        subject: Email subject
        message: Email message
        recipient_list: List of recipient emails
        from_email: Sender email (optional)
    """
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def get_client_ip(request):
    """
    Get client IP address from request
    الحصول على عنوان IP للعميل من الطلب
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_working_days(start_date, end_date, exclude_weekends=True):
    """
    Calculate working days between two dates
    حساب أيام العمل بين تاريخين
    
    Args:
        start_date: Start date
        end_date: End date
        exclude_weekends: Whether to exclude weekends (Friday and Saturday for Arabic countries)
    
    Returns:
        Number of working days
    """
    from datetime import timedelta
    
    if start_date > end_date:
        return 0
    
    days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if exclude_weekends:
            # Friday = 4, Saturday = 5 in Python's weekday()
            if current_date.weekday() not in [4, 5]:
                days += 1
        else:
            days += 1
        current_date += timedelta(days=1)
    
    return days


def format_currency(amount, currency='ر.س'):
    """
    Format amount as currency
    تنسيق المبلغ كعملة
    
    Args:
        amount: Amount to format
        currency: Currency symbol (default: Saudi Riyal)
    
    Returns:
        Formatted currency string
    """
    try:
        return f"{amount:,.2f} {currency}"
    except:
        return f"{amount} {currency}"


def get_fiscal_year(date=None):
    """
    Get fiscal year for a given date
    الحصول على السنة المالية لتاريخ معين
    
    Args:
        date: Date to get fiscal year for (default: today)
    
    Returns:
        Tuple of (start_date, end_date) for fiscal year
    """
    from datetime import date as dt_date
    
    if date is None:
        date = timezone.now().date()
    
    # Assuming fiscal year starts on January 1st
    if isinstance(date, dt_date):
        year = date.year
    else:
        year = date.year
    
    start_date = dt_date(year, 1, 1)
    end_date = dt_date(year, 12, 31)
    
    return start_date, end_date


def generate_employee_code(prefix='EMP'):
    """
    Generate unique employee code
    إنشاء رمز موظف فريد
    
    Args:
        prefix: Prefix for employee code
    
    Returns:
        Unique employee code
    """
    from employees.models import Employee
    import random
    
    while True:
        code = f"{prefix}{random.randint(10000, 99999)}"
        if not Employee.objects.filter(emp_code=code).exists():
            return code


def validate_national_id(national_id):
    """
    Validate national ID format
    التحقق من صحة تنسيق الهوية الوطنية
    
    Args:
        national_id: National ID to validate
    
    Returns:
        Boolean indicating if valid
    """
    # Basic validation - adjust based on your country's format
    if not national_id:
        return False
    
    # Remove any spaces or dashes
    national_id = national_id.replace(' ', '').replace('-', '')
    
    # Check if it's numeric and has correct length (e.g., 10 digits for Saudi Arabia)
    if not national_id.isdigit():
        return False
    
    if len(national_id) != 10:
        return False
    
    return True


class PermissionMixin:
    """
    Mixin for permission checking
    خليط للتحقق من الأذونات
    """
    
    def check_permission(self, user, permission):
        """Check if user has permission"""
        if user.role == 'admin':
            return True
        
        # Add more permission logic here
        return False
    
    def check_object_permission(self, user, obj):
        """Check if user has permission for specific object"""
        if user.role == 'admin':
            return True
        
        # Add more permission logic here
        return False

