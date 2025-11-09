"""
Celery configuration for HR_sys project
إعدادات Celery لمشروع نظام الموارد البشرية
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HR_sys.settings')

# Create Celery app
app = Celery('HR_sys')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    # Sync ZK devices every 30 minutes
    'sync-zk-devices-every-30-minutes': {
        'task': 'attendance.sync_zk_devices',
        'schedule': crontab(minute='*/30'),
        'args': (1, True),  # Sync last 1 day, auto-process
    },
    
    # Process attendance logs every 15 minutes
    'process-attendance-logs-every-15-minutes': {
        'task': 'attendance.process_attendance_logs',
        'schedule': crontab(minute='*/15'),
    },
    
    # Calculate daily attendance at 11:00 PM
    'calculate-daily-attendance-at-11pm': {
        'task': 'attendance.calculate_daily_attendance',
        'schedule': crontab(hour=23, minute=0),
    },
    
    # Send late notifications at 9:30 AM
    'send-late-notifications-at-9-30am': {
        'task': 'attendance.send_late_notifications',
        'schedule': crontab(hour=9, minute=30),
    },
}

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Africa/Cairo',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')

