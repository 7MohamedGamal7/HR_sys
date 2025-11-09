"""
Celery tasks for attendance app
مهام Celery لتطبيق الحضور
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name='attendance.sync_zk_devices')
def sync_zk_devices_task(days=None, auto_process=True):
    """
    Celery task to sync ZK devices
    مهمة Celery لمزامنة أجهزة البصمة
    
    Args:
        days: Number of days to sync (None = all)
        auto_process: Whether to auto-process logs
        
    Returns:
        Dictionary with sync results
    """
    from attendance.zk_integration import sync_all_devices
    
    try:
        logger.info("Starting scheduled ZK device sync")
        
        # Calculate date range if specified
        start_date = None
        end_date = None
        
        if days:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=days)
        
        # Perform sync
        results = sync_all_devices(start_date, end_date, auto_process)
        
        logger.info(
            f"Scheduled sync completed: {results['total_success']} new records, "
            f"{results['total_errors']} errors"
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error in scheduled sync: {str(e)}")
        raise


@shared_task(name='attendance.process_attendance_logs')
def process_attendance_logs_task(employee_id=None, date=None):
    """
    Celery task to process unprocessed attendance logs
    مهمة Celery لمعالجة سجلات الحضور غير المعالجة
    
    Args:
        employee_id: Optional employee ID
        date: Optional date
        
    Returns:
        Dictionary with processing statistics
    """
    from attendance.zk_integration import ZKDeviceManager
    
    try:
        logger.info("Starting scheduled attendance log processing")
        
        manager = ZKDeviceManager('', 0)  # Dummy instance for processing
        stats = manager.process_attendance_logs(employee_id, date)
        
        logger.info(
            f"Scheduled processing completed: {stats['processed_logs']} logs processed"
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error in scheduled processing: {str(e)}")
        raise


@shared_task(name='attendance.calculate_daily_attendance')
def calculate_daily_attendance_task(date=None):
    """
    Celery task to calculate daily attendance for all employees
    مهمة Celery لحساب الحضور اليومي لجميع الموظفين
    
    Args:
        date: Date to calculate (default: yesterday)
        
    Returns:
        Dictionary with calculation results
    """
    from attendance.models import Attendance
    from employees.models import Employee
    from django.db.models import Q
    
    try:
        # Default to yesterday if no date specified
        if date is None:
            date = (timezone.now() - timedelta(days=1)).date()
        
        logger.info(f"Calculating daily attendance for {date}")
        
        stats = {
            'date': str(date),
            'total_employees': 0,
            'present': 0,
            'absent': 0,
            'late': 0,
            'on_leave': 0
        }
        
        # Get all active employees
        employees = Employee.objects.filter(is_active=True)
        stats['total_employees'] = employees.count()
        
        for employee in employees:
            # Check if attendance record exists
            attendance = Attendance.objects.filter(
                employee=employee,
                date=date
            ).first()
            
            if attendance:
                # Update status count
                if attendance.status == 'present':
                    stats['present'] += 1
                elif attendance.status == 'absent':
                    stats['absent'] += 1
                elif attendance.status == 'late':
                    stats['late'] += 1
                elif attendance.status == 'on_leave':
                    stats['on_leave'] += 1
            else:
                # Check if employee has approved leave
                from attendance.models import LeaveRequest
                has_leave = LeaveRequest.objects.filter(
                    employee=employee,
                    start_date__lte=date,
                    end_date__gte=date,
                    status='approved'
                ).exists()
                
                if has_leave:
                    # Create attendance record with on_leave status
                    Attendance.objects.create(
                        employee=employee,
                        date=date,
                        status='on_leave'
                    )
                    stats['on_leave'] += 1
                else:
                    # Mark as absent
                    Attendance.objects.create(
                        employee=employee,
                        date=date,
                        status='absent'
                    )
                    stats['absent'] += 1
        
        logger.info(
            f"Daily attendance calculated for {date}: "
            f"{stats['present']} present, {stats['absent']} absent, "
            f"{stats['late']} late, {stats['on_leave']} on leave"
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error calculating daily attendance: {str(e)}")
        raise


@shared_task(name='attendance.send_late_notifications')
def send_late_notifications_task(date=None):
    """
    Celery task to send notifications for late employees
    مهمة Celery لإرسال إشعارات للموظفين المتأخرين
    
    Args:
        date: Date to check (default: today)
        
    Returns:
        Number of notifications sent
    """
    from attendance.models import Attendance
    from core.utils import create_notification
    
    try:
        # Default to today if no date specified
        if date is None:
            date = timezone.now().date()
        
        logger.info(f"Sending late notifications for {date}")
        
        # Get all late attendance records
        late_attendance = Attendance.objects.filter(
            date=date,
            status='late',
            late_minutes__gt=0
        ).select_related('employee')
        
        notifications_sent = 0
        
        for attendance in late_attendance:
            employee = attendance.employee
            
            # Create notification for employee
            if hasattr(employee, 'user_account') and employee.user_account:
                create_notification(
                    user=employee.user_account,
                    title='تأخير في الحضور',
                    message=f'تم تسجيل تأخير {attendance.late_minutes} دقيقة في تاريخ {date}',
                    notification_type='warning'
                )
                notifications_sent += 1
            
            # Create notification for manager
            if employee.manager and hasattr(employee.manager, 'user_account') and employee.manager.user_account:
                create_notification(
                    user=employee.manager.user_account,
                    title='تأخير موظف',
                    message=f'الموظف {employee.get_full_name_ar()} تأخر {attendance.late_minutes} دقيقة',
                    notification_type='info'
                )
                notifications_sent += 1
        
        logger.info(f"Sent {notifications_sent} late notifications for {date}")
        
        return notifications_sent
        
    except Exception as e:
        logger.error(f"Error sending late notifications: {str(e)}")
        raise

