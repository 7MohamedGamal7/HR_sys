"""
ZK Fingerprint Device Integration
تكامل جهاز البصمة ZK
"""
from django.utils import timezone
from django.db import transaction
from .models import AttendanceLog, Attendance
from employees.models import Employee
import logging

logger = logging.getLogger(__name__)


class ZKDeviceManager:
    """
    Manager for ZK fingerprint device integration
    مدير تكامل جهاز البصمة ZK
    """
    
    def __init__(self, ip_address, port=4370):
        """
        Initialize ZK device connection
        
        Args:
            ip_address: IP address of the ZK device
            port: Port number (default: 4370)
        """
        self.ip_address = ip_address
        self.port = port
        self.conn = None
        self.zk = None
    
    def connect(self):
        """
        Connect to ZK device
        الاتصال بجهاز البصمة
        """
        try:
            from zk import ZK
            
            self.zk = ZK(self.ip_address, port=self.port, timeout=5)
            self.conn = self.zk.connect()
            logger.info(f"Connected to ZK device at {self.ip_address}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to ZK device: {e}")
            return False
    
    def disconnect(self):
        """
        Disconnect from ZK device
        قطع الاتصال بجهاز البصمة
        """
        try:
            if self.conn:
                self.conn.disconnect()
                logger.info("Disconnected from ZK device")
        except Exception as e:
            logger.error(f"Error disconnecting from ZK device: {e}")
    
    def get_attendance_logs(self):
        """
        Fetch attendance logs from ZK device
        جلب سجلات الحضور من جهاز البصمة
        
        Returns:
            List of attendance records
        """
        if not self.conn:
            logger.error("Not connected to ZK device")
            return []
        
        try:
            attendance_records = self.conn.get_attendance()
            logger.info(f"Fetched {len(attendance_records)} attendance records")
            return attendance_records
        except Exception as e:
            logger.error(f"Error fetching attendance logs: {e}")
            return []
    
    def sync_attendance_logs(self):
        """
        Sync attendance logs from ZK device to database
        مزامنة سجلات الحضور من جهاز البصمة إلى قاعدة البيانات
        
        Returns:
            Tuple of (success_count, error_count)
        """
        if not self.connect():
            return 0, 0
        
        success_count = 0
        error_count = 0
        
        try:
            attendance_records = self.get_attendance_logs()
            
            for record in attendance_records:
                try:
                    # Find employee by ZK user ID
                    employee = Employee.objects.get(
                        zk_user_id=str(record.user_id),
                        is_active=True
                    )
                    
                    # Create attendance log
                    log, created = AttendanceLog.objects.get_or_create(
                        employee=employee,
                        timestamp=record.timestamp,
                        defaults={
                            'device_id': self.ip_address,
                            'punch_type': self._determine_punch_type(record),
                            'is_processed': False,
                        }
                    )
                    
                    if created:
                        success_count += 1
                        logger.info(f"Created attendance log for {employee.emp_code} at {record.timestamp}")
                    
                except Employee.DoesNotExist:
                    logger.warning(f"Employee with ZK user ID {record.user_id} not found")
                    error_count += 1
                except Exception as e:
                    logger.error(f"Error processing attendance record: {e}")
                    error_count += 1
            
        finally:
            self.disconnect()
        
        return success_count, error_count
    
    def _determine_punch_type(self, record):
        """
        Determine punch type from record
        تحديد نوع التسجيل من السجل
        """
        # This is a simplified version - adjust based on your ZK device configuration
        # Some devices have punch state: 0=check-in, 1=check-out, etc.
        if hasattr(record, 'punch'):
            if record.punch == 0:
                return 'check_in'
            elif record.punch == 1:
                return 'check_out'
        
        # Default logic: determine based on time
        hour = record.timestamp.hour
        if hour < 12:
            return 'check_in'
        else:
            return 'check_out'
    
    def process_attendance_logs(self):
        """
        Process unprocessed attendance logs and create attendance records
        معالجة سجلات الحضور غير المعالجة وإنشاء سجلات الحضور
        
        Returns:
            Number of processed logs
        """
        unprocessed_logs = AttendanceLog.objects.filter(is_processed=False).order_by('timestamp')
        processed_count = 0
        
        # Group logs by employee and date
        from collections import defaultdict
        logs_by_employee_date = defaultdict(list)
        
        for log in unprocessed_logs:
            key = (log.employee.id, log.timestamp.date())
            logs_by_employee_date[key].append(log)
        
        # Process each employee-date group
        for (employee_id, date), logs in logs_by_employee_date.items():
            try:
                with transaction.atomic():
                    employee = Employee.objects.get(id=employee_id)
                    
                    # Get or create attendance record
                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=date,
                        defaults={
                            'status': 'present',
                        }
                    )
                    
                    # Find check-in and check-out times
                    check_in_logs = [l for l in logs if l.punch_type == 'check_in']
                    check_out_logs = [l for l in logs if l.punch_type == 'check_out']
                    
                    if check_in_logs:
                        attendance.check_in = min(log.timestamp for log in check_in_logs)
                    
                    if check_out_logs:
                        attendance.check_out = max(log.timestamp for log in check_out_logs)
                    
                    # Calculate work hours and late minutes
                    if attendance.check_in and attendance.check_out:
                        attendance.calculate_work_hours()
                        
                        # Calculate late minutes
                        if employee.work_shift:
                            expected_time = timezone.datetime.combine(
                                date,
                                employee.work_shift.start_time
                            )
                            expected_time = timezone.make_aware(expected_time)
                            
                            if attendance.check_in > expected_time:
                                late_delta = attendance.check_in - expected_time
                                attendance.late_minutes = int(late_delta.total_seconds() / 60)
                    
                    attendance.save()
                    
                    # Mark logs as processed
                    for log in logs:
                        log.is_processed = True
                        log.processed_at = timezone.now()
                        log.save()
                    
                    processed_count += len(logs)
                    logger.info(f"Processed {len(logs)} logs for {employee.emp_code} on {date}")
                    
            except Exception as e:
                logger.error(f"Error processing logs for employee {employee_id} on {date}: {e}")
        
        return processed_count
    
    def get_users(self):
        """
        Get all users from ZK device
        الحصول على جميع المستخدمين من جهاز البصمة
        """
        if not self.conn:
            if not self.connect():
                return []
        
        try:
            users = self.conn.get_users()
            return users
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return []
        finally:
            self.disconnect()
    
    def add_user(self, user_id, name, privilege=0, password='', group_id='', user_id_str=''):
        """
        Add user to ZK device
        إضافة مستخدم إلى جهاز البصمة
        """
        if not self.conn:
            if not self.connect():
                return False
        
        try:
            self.conn.set_user(
                uid=user_id,
                name=name,
                privilege=privilege,
                password=password,
                group_id=group_id,
                user_id=user_id_str
            )
            logger.info(f"Added user {name} (ID: {user_id}) to ZK device")
            return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False
        finally:
            self.disconnect()
    
    def delete_user(self, user_id):
        """
        Delete user from ZK device
        حذف مستخدم من جهاز البصمة
        """
        if not self.conn:
            if not self.connect():
                return False
        
        try:
            self.conn.delete_user(uid=user_id)
            logger.info(f"Deleted user ID {user_id} from ZK device")
            return True
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
        finally:
            self.disconnect()


def sync_all_devices():
    """
    Sync attendance from all configured ZK devices
    مزامنة الحضور من جميع أجهزة البصمة المكونة
    """
    from core.models import SystemSettings
    
    # Get device configurations from settings
    # Format: "ip1:port1,ip2:port2,..."
    devices_config = SystemSettings.objects.filter(key='zk_devices').first()
    
    if not devices_config:
        logger.warning("No ZK devices configured")
        return
    
    devices = devices_config.value.split(',')
    total_success = 0
    total_errors = 0
    
    for device in devices:
        try:
            parts = device.strip().split(':')
            ip = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 4370
            
            manager = ZKDeviceManager(ip, port)
            success, errors = manager.sync_attendance_logs()
            total_success += success
            total_errors += errors
            
        except Exception as e:
            logger.error(f"Error syncing device {device}: {e}")
            total_errors += 1
    
    logger.info(f"Sync completed: {total_success} success, {total_errors} errors")
    
    # Process the synced logs
    manager = ZKDeviceManager('', 0)  # Dummy instance for processing
    processed = manager.process_attendance_logs()
    logger.info(f"Processed {processed} attendance logs")

