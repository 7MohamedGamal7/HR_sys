"""
Enhanced ZK Fingerprint Device Integration
تكامل محسّن لجهاز البصمة ZK

Features:
- Robust error handling and retry logic
- Data validation before saving
- Duplicate record handling
- Proper timezone handling
- Comprehensive logging
- Connection pooling for multiple devices
- Transaction management
"""
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from .models import AttendanceLog, Attendance
from employees.models import Employee
from core.models import SystemSettings
import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict
import time

logger = logging.getLogger(__name__)


class ZKDeviceError(Exception):
    """Custom exception for ZK device errors"""
    pass


class ZKDeviceManager:
    """
    Enhanced manager for ZK fingerprint device integration
    مدير محسّن لتكامل جهاز البصمة ZK
    """

    # Connection retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    CONNECTION_TIMEOUT = 10  # seconds

    def __init__(self, ip_address: str, port: int = 4370, device_name: str = None):
        """
        Initialize ZK device connection

        Args:
            ip_address: IP address of the ZK device
            port: Port number (default: 4370)
            device_name: Optional friendly name for the device
        """
        self.ip_address = ip_address
        self.port = port
        self.device_name = device_name or f"{ip_address}:{port}"
        self.conn = None
        self.zk = None
        self._connection_status = False

    def connect(self, retry: bool = True) -> bool:
        """
        Connect to ZK device with retry logic
        الاتصال بجهاز البصمة مع إعادة المحاولة

        Args:
            retry: Whether to retry on failure

        Returns:
            bool: True if connected successfully
        """
        attempts = self.MAX_RETRIES if retry else 1

        for attempt in range(1, attempts + 1):
            try:
                from zk import ZK

                logger.info(f"Attempting to connect to {self.device_name} (attempt {attempt}/{attempts})")

                self.zk = ZK(
                    self.ip_address,
                    port=self.port,
                    timeout=self.CONNECTION_TIMEOUT,
                    password=0,
                    force_udp=False,
                    ommit_ping=False
                )
                self.conn = self.zk.connect()
                self._connection_status = True

                # Disable device to prevent interference during data transfer
                self.conn.disable_device()

                logger.info(f"✓ Successfully connected to {self.device_name}")
                return True

            except ImportError:
                logger.error("pyzk library not installed. Run: pip install pyzk")
                return False

            except Exception as e:
                logger.warning(f"Connection attempt {attempt} failed for {self.device_name}: {str(e)}")

                if attempt < attempts:
                    logger.info(f"Retrying in {self.RETRY_DELAY} seconds...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    logger.error(f"✗ Failed to connect to {self.device_name} after {attempts} attempts")
                    self._connection_status = False
                    return False

        return False

    def disconnect(self) -> None:
        """
        Safely disconnect from ZK device
        قطع الاتصال بأمان من جهاز البصمة
        """
        try:
            if self.conn:
                # Re-enable device before disconnecting
                self.conn.enable_device()
                self.conn.disconnect()
                self._connection_status = False
                logger.info(f"✓ Disconnected from {self.device_name}")
        except Exception as e:
            logger.error(f"Error disconnecting from {self.device_name}: {str(e)}")

    def is_connected(self) -> bool:
        """Check if device is connected"""
        return self._connection_status and self.conn is not None

    def get_device_info(self) -> Optional[Dict]:
        """
        Get device information
        الحصول على معلومات الجهاز

        Returns:
            Dictionary with device info or None
        """
        if not self.is_connected():
            logger.error(f"Not connected to {self.device_name}")
            return None

        try:
            info = {
                'device_name': self.device_name,
                'ip_address': self.ip_address,
                'port': self.port,
                'serial_number': self.conn.get_serialnumber(),
                'platform': self.conn.get_platform(),
                'firmware_version': self.conn.get_firmware_version(),
                'device_time': self.conn.get_time(),
                'users_count': len(self.conn.get_users()),
                'records_count': len(self.conn.get_attendance()),
            }
            return info
        except Exception as e:
            logger.error(f"Error getting device info: {str(e)}")
            return None

    def get_attendance_logs(self, start_date: datetime = None, end_date: datetime = None) -> List:
        """
        Fetch attendance logs from ZK device with optional date filtering
        جلب سجلات الحضور من جهاز البصمة مع تصفية اختيارية بالتاريخ

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of attendance records
        """
        if not self.is_connected():
            logger.error(f"Not connected to {self.device_name}")
            return []

        try:
            attendance_records = self.conn.get_attendance()
            logger.info(f"Fetched {len(attendance_records)} raw attendance records from {self.device_name}")

            # Filter by date if specified
            if start_date or end_date:
                filtered_records = []
                for record in attendance_records:
                    record_date = record.timestamp

                    if start_date and record_date < start_date:
                        continue
                    if end_date and record_date > end_date:
                        continue

                    filtered_records.append(record)

                logger.info(f"Filtered to {len(filtered_records)} records within date range")
                return filtered_records

            return attendance_records

        except Exception as e:
            logger.error(f"Error fetching attendance logs from {self.device_name}: {str(e)}")
            return []

    def validate_attendance_record(self, record, employee: Employee) -> Tuple[bool, str]:
        """
        Validate attendance record before saving
        التحقق من صحة سجل الحضور قبل الحفظ

        Args:
            record: ZK attendance record
            employee: Employee object

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if timestamp is valid
            if not hasattr(record, 'timestamp') or not record.timestamp:
                return False, "Missing timestamp"

            # Check if timestamp is in the future
            if record.timestamp > timezone.now():
                return False, f"Timestamp is in the future: {record.timestamp}"

            # Check if timestamp is too old (more than 1 year)
            one_year_ago = timezone.now() - timedelta(days=365)
            if record.timestamp < one_year_ago:
                return False, f"Timestamp is too old: {record.timestamp}"

            # Check if employee is active
            if not employee.is_active:
                return False, f"Employee {employee.emp_code} is not active"

            return True, ""

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def sync_attendance_logs(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, int]:
        """
        Sync attendance logs from ZK device to database with enhanced error handling
        مزامنة سجلات الحضور من جهاز البصمة إلى قاعدة البيانات مع معالجة محسّنة للأخطاء

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            Dictionary with sync statistics
        """
        stats = {
            'success': 0,
            'duplicates': 0,
            'errors': 0,
            'invalid': 0,
            'employee_not_found': 0,
            'total_fetched': 0
        }

        if not self.connect():
            logger.error(f"Failed to connect to {self.device_name}")
            return stats

        try:
            # Fetch attendance records
            attendance_records = self.get_attendance_logs(start_date, end_date)
            stats['total_fetched'] = len(attendance_records)

            if not attendance_records:
                logger.warning(f"No attendance records found on {self.device_name}")
                return stats

            logger.info(f"Processing {len(attendance_records)} records from {self.device_name}")

            # Process each record
            for record in attendance_records:
                try:
                    # Find employee by ZK user ID
                    try:
                        employee = Employee.objects.get(
                            zk_user_id=str(record.user_id),
                            is_active=True
                        )
                    except Employee.DoesNotExist:
                        logger.warning(
                            f"Employee with ZK user ID {record.user_id} not found "
                            f"(Device: {self.device_name})"
                        )
                        stats['employee_not_found'] += 1
                        continue

                    # Validate record
                    is_valid, error_msg = self.validate_attendance_record(record, employee)
                    if not is_valid:
                        logger.warning(
                            f"Invalid record for {employee.emp_code}: {error_msg} "
                            f"(Device: {self.device_name})"
                        )
                        stats['invalid'] += 1
                        continue

                    # Make timestamp timezone-aware
                    timestamp = record.timestamp
                    if timezone.is_naive(timestamp):
                        timestamp = timezone.make_aware(timestamp)

                    # Determine punch type
                    punch_type = self._determine_punch_type(record, employee, timestamp)

                    # Create or update attendance log (handle duplicates)
                    with transaction.atomic():
                        log, created = AttendanceLog.objects.get_or_create(
                            employee=employee,
                            timestamp=timestamp,
                            device_id=self.device_name,
                            defaults={
                                'punch_type': punch_type,
                                'is_processed': False,
                            }
                        )

                        if created:
                            stats['success'] += 1
                            logger.debug(
                                f"✓ Created log: {employee.emp_code} at {timestamp} "
                                f"({punch_type})"
                            )
                        else:
                            stats['duplicates'] += 1
                            logger.debug(
                                f"Duplicate log skipped: {employee.emp_code} at {timestamp}"
                            )

                except Exception as e:
                    logger.error(
                        f"Error processing record (user_id: {getattr(record, 'user_id', 'unknown')}): "
                        f"{str(e)}"
                    )
                    stats['errors'] += 1

            # Log summary
            logger.info(
                f"Sync completed for {self.device_name}: "
                f"{stats['success']} new, {stats['duplicates']} duplicates, "
                f"{stats['errors']} errors, {stats['invalid']} invalid, "
                f"{stats['employee_not_found']} employee not found"
            )

        except Exception as e:
            logger.error(f"Critical error during sync from {self.device_name}: {str(e)}")
            stats['errors'] += 1

        finally:
            self.disconnect()

        return stats

    def _determine_punch_type(self, record, employee: Employee, timestamp: datetime) -> str:
        """
        Intelligently determine punch type from record
        تحديد نوع التسجيل بذكاء من السجل

        Args:
            record: ZK attendance record
            employee: Employee object
            timestamp: Timestamp of the record

        Returns:
            Punch type: 'check_in', 'check_out', 'break_out', or 'break_in'
        """
        # Method 1: Check if device provides punch state
        if hasattr(record, 'punch'):
            punch_state = record.punch
            if punch_state == 0:
                return 'check_in'
            elif punch_state == 1:
                return 'check_out'
            elif punch_state == 2:
                return 'break_out'
            elif punch_state == 3:
                return 'break_in'

        # Method 2: Check if device provides status
        if hasattr(record, 'status'):
            status = record.status
            if status == 0:
                return 'check_in'
            elif status == 1:
                return 'check_out'

        # Method 3: Intelligent determination based on context
        date = timestamp.date()

        # Get existing logs for this employee on this date
        existing_logs = AttendanceLog.objects.filter(
            employee=employee,
            timestamp__date=date
        ).order_by('timestamp')

        if not existing_logs.exists():
            # First log of the day is always check-in
            return 'check_in'

        # Get the last log
        last_log = existing_logs.last()

        # Alternate between check-in and check-out
        if last_log.punch_type in ['check_in', 'break_in']:
            return 'check_out'
        else:
            return 'check_in'

    def process_attendance_logs(self, employee_id: int = None, date: datetime = None) -> Dict[str, int]:
        """
        Process unprocessed attendance logs and create/update attendance records
        معالجة سجلات الحضور غير المعالجة وإنشاء/تحديث سجلات الحضور

        Args:
            employee_id: Optional employee ID to process specific employee
            date: Optional date to process specific date

        Returns:
            Dictionary with processing statistics
        """
        stats = {
            'processed_logs': 0,
            'created_attendance': 0,
            'updated_attendance': 0,
            'errors': 0
        }

        # Build query for unprocessed logs
        query = AttendanceLog.objects.filter(is_processed=False)

        if employee_id:
            query = query.filter(employee_id=employee_id)

        if date:
            query = query.filter(timestamp__date=date)

        unprocessed_logs = query.order_by('timestamp')

        if not unprocessed_logs.exists():
            logger.info("No unprocessed attendance logs found")
            return stats

        logger.info(f"Processing {unprocessed_logs.count()} unprocessed logs")

        # Group logs by employee and date
        from collections import defaultdict
        logs_by_employee_date = defaultdict(list)

        for log in unprocessed_logs:
            key = (log.employee.id, log.timestamp.date())
            logs_by_employee_date[key].append(log)

        # Process each employee-date group
        for (emp_id, log_date), logs in logs_by_employee_date.items():
            try:
                with transaction.atomic():
                    employee = Employee.objects.get(id=emp_id)

                    # Get or create attendance record
                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=log_date,
                        defaults={
                            'status': 'present',
                        }
                    )

                    if created:
                        stats['created_attendance'] += 1
                    else:
                        stats['updated_attendance'] += 1

                    # Find check-in and check-out times
                    check_in_logs = [l for l in logs if l.punch_type == 'check_in']
                    check_out_logs = [l for l in logs if l.punch_type == 'check_out']

                    # Set check-in time (earliest check-in)
                    if check_in_logs:
                        earliest_check_in = min(log.timestamp for log in check_in_logs)
                        attendance.check_in = earliest_check_in

                    # Set check-out time (latest check-out)
                    if check_out_logs:
                        latest_check_out = max(log.timestamp for log in check_out_logs)
                        attendance.check_out = latest_check_out

                    # Calculate work hours
                    if attendance.check_in and attendance.check_out:
                        attendance.calculate_work_hours()

                        # Calculate late minutes
                        if employee.work_shift:
                            expected_time = timezone.datetime.combine(
                                log_date,
                                employee.work_shift.start_time
                            )
                            expected_time = timezone.make_aware(expected_time)

                            if attendance.check_in > expected_time:
                                late_delta = attendance.check_in - expected_time
                                attendance.late_minutes = int(late_delta.total_seconds() / 60)

                                # Update status if late
                                if attendance.late_minutes > 0:
                                    attendance.status = 'late'

                            # Calculate early leave minutes
                            expected_end_time = timezone.datetime.combine(
                                log_date,
                                employee.work_shift.end_time
                            )
                            expected_end_time = timezone.make_aware(expected_end_time)

                            if attendance.check_out < expected_end_time:
                                early_delta = expected_end_time - attendance.check_out
                                attendance.early_leave_minutes = int(early_delta.total_seconds() / 60)

                            # Calculate overtime
                            if attendance.check_out > expected_end_time:
                                overtime_delta = attendance.check_out - expected_end_time
                                attendance.overtime_hours = round(overtime_delta.total_seconds() / 3600, 2)

                    attendance.save()

                    # Mark logs as processed
                    for log in logs:
                        log.is_processed = True
                        log.processed_at = timezone.now()
                        log.save()

                    stats['processed_logs'] += len(logs)
                    logger.debug(
                        f"✓ Processed {len(logs)} logs for {employee.emp_code} on {log_date}"
                    )

            except Employee.DoesNotExist:
                logger.error(f"Employee with ID {emp_id} not found")
                stats['errors'] += 1
            except Exception as e:
                logger.error(
                    f"Error processing logs for employee {emp_id} on {log_date}: {str(e)}"
                )
                stats['errors'] += 1

        logger.info(
            f"Processing completed: {stats['processed_logs']} logs processed, "
            f"{stats['created_attendance']} attendance created, "
            f"{stats['updated_attendance']} attendance updated, "
            f"{stats['errors']} errors"
        )

        return stats

    def get_users(self) -> List:
        """
        Get all users from ZK device
        الحصول على جميع المستخدمين من جهاز البصمة

        Returns:
            List of user objects
        """
        if not self.is_connected():
            if not self.connect():
                return []

        try:
            users = self.conn.get_users()
            logger.info(f"Fetched {len(users)} users from {self.device_name}")
            return users
        except Exception as e:
            logger.error(f"Error fetching users from {self.device_name}: {str(e)}")
            return []
        finally:
            self.disconnect()

    def add_user(self, user_id: int, name: str, privilege: int = 0,
                 password: str = '', group_id: str = '', user_id_str: str = '') -> bool:
        """
        Add user to ZK device
        إضافة مستخدم إلى جهاز البصمة

        Args:
            user_id: Numeric user ID
            name: User name
            privilege: User privilege level (0=user, 14=admin)
            password: Optional password
            group_id: Optional group ID
            user_id_str: Optional string user ID

        Returns:
            bool: True if successful
        """
        if not self.is_connected():
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
            logger.info(f"✓ Added user {name} (ID: {user_id}) to {self.device_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding user to {self.device_name}: {str(e)}")
            return False
        finally:
            self.disconnect()

    def delete_user(self, user_id: int) -> bool:
        """
        Delete user from ZK device
        حذف مستخدم من جهاز البصمة

        Args:
            user_id: Numeric user ID to delete

        Returns:
            bool: True if successful
        """
        if not self.is_connected():
            if not self.connect():
                return False

        try:
            self.conn.delete_user(uid=user_id)
            logger.info(f"✓ Deleted user ID {user_id} from {self.device_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting user from {self.device_name}: {str(e)}")
            return False
        finally:
            self.disconnect()

    def sync_employee_to_device(self, employee: Employee) -> bool:
        """
        Sync employee to ZK device
        مزامنة الموظف إلى جهاز البصمة

        Args:
            employee: Employee object

        Returns:
            bool: True if successful
        """
        if not employee.zk_user_id:
            logger.error(f"Employee {employee.emp_code} has no ZK user ID")
            return False

        try:
            user_id = int(employee.zk_user_id)
            name = employee.get_full_name_en() or employee.get_full_name_ar()

            return self.add_user(
                user_id=user_id,
                name=name[:24],  # ZK devices have name length limit
                privilege=0
            )
        except ValueError:
            logger.error(f"Invalid ZK user ID for employee {employee.emp_code}: {employee.zk_user_id}")
            return False

    def clear_attendance_logs(self) -> bool:
        """
        Clear all attendance logs from device (use with caution!)
        مسح جميع سجلات الحضور من الجهاز (استخدم بحذر!)

        Returns:
            bool: True if successful
        """
        if not self.is_connected():
            if not self.connect():
                return False

        try:
            self.conn.clear_attendance()
            logger.warning(f"⚠ Cleared all attendance logs from {self.device_name}")
            return True
        except Exception as e:
            logger.error(f"Error clearing attendance logs from {self.device_name}: {str(e)}")
            return False
        finally:
            self.disconnect()



# ============================================================================
# Utility Functions
# ============================================================================

def get_configured_devices() -> List[Dict[str, any]]:
    """
    Get list of configured ZK devices from system settings
    الحصول على قائمة أجهزة البصمة المكونة من إعدادات النظام

    Returns:
        List of device configurations
    """
    devices = []

    try:
        # Get device configurations from settings
        # Format: "name1|ip1:port1,name2|ip2:port2,..."
        devices_config = SystemSettings.objects.filter(key='zk_devices').first()

        if not devices_config or not devices_config.value:
            logger.warning("No ZK devices configured in system settings")
            return devices

        device_strings = devices_config.value.split(',')

        for device_str in device_strings:
            try:
                device_str = device_str.strip()

                # Check if device has a name
                if '|' in device_str:
                    name, address = device_str.split('|', 1)
                else:
                    name = None
                    address = device_str

                # Parse IP and port
                if ':' in address:
                    ip, port = address.split(':', 1)
                    port = int(port)
                else:
                    ip = address
                    port = 4370

                devices.append({
                    'name': name or f"{ip}:{port}",
                    'ip': ip,
                    'port': port
                })

            except Exception as e:
                logger.error(f"Error parsing device configuration '{device_str}': {str(e)}")

    except Exception as e:
        logger.error(f"Error getting configured devices: {str(e)}")

    return devices


def sync_all_devices(start_date: datetime = None, end_date: datetime = None,
                     auto_process: bool = True) -> Dict[str, any]:
    """
    Sync attendance from all configured ZK devices
    مزامنة الحضور من جميع أجهزة البصمة المكونة

    Args:
        start_date: Optional start date for filtering
        end_date: Optional end date for filtering
        auto_process: Whether to automatically process logs after sync

    Returns:
        Dictionary with sync results
    """
    results = {
        'devices_synced': 0,
        'devices_failed': 0,
        'total_success': 0,
        'total_duplicates': 0,
        'total_errors': 0,
        'total_invalid': 0,
        'total_employee_not_found': 0,
        'total_fetched': 0,
        'processing_stats': None,
        'device_results': []
    }

    # Get configured devices
    devices = get_configured_devices()

    if not devices:
        logger.warning("No ZK devices configured")
        return results

    logger.info(f"Starting sync for {len(devices)} configured devices")

    # Sync each device
    for device_config in devices:
        device_name = device_config['name']
        ip = device_config['ip']
        port = device_config['port']

        try:
            logger.info(f"Syncing device: {device_name}")

            manager = ZKDeviceManager(ip, port, device_name)
            stats = manager.sync_attendance_logs(start_date, end_date)

            # Aggregate statistics
            results['total_success'] += stats['success']
            results['total_duplicates'] += stats['duplicates']
            results['total_errors'] += stats['errors']
            results['total_invalid'] += stats['invalid']
            results['total_employee_not_found'] += stats['employee_not_found']
            results['total_fetched'] += stats['total_fetched']
            results['devices_synced'] += 1

            # Store device-specific results
            results['device_results'].append({
                'device': device_name,
                'status': 'success',
                'stats': stats
            })

            logger.info(f"✓ Completed sync for {device_name}")

        except Exception as e:
            logger.error(f"✗ Error syncing device {device_name}: {str(e)}")
            results['devices_failed'] += 1
            results['device_results'].append({
                'device': device_name,
                'status': 'failed',
                'error': str(e)
            })

    # Log summary
    logger.info(
        f"Sync summary: {results['devices_synced']} devices synced, "
        f"{results['devices_failed']} failed, "
        f"{results['total_success']} new records, "
        f"{results['total_duplicates']} duplicates, "
        f"{results['total_errors']} errors"
    )

    # Auto-process logs if enabled
    if auto_process and results['total_success'] > 0:
        logger.info("Auto-processing synced logs...")
        manager = ZKDeviceManager('', 0)  # Dummy instance for processing
        processing_stats = manager.process_attendance_logs()
        results['processing_stats'] = processing_stats
        logger.info(
            f"Processing completed: {processing_stats['processed_logs']} logs processed"
        )

    return results


def test_device_connection(ip: str, port: int = 4370) -> Dict[str, any]:
    """
    Test connection to a ZK device
    اختبار الاتصال بجهاز البصمة

    Args:
        ip: Device IP address
        port: Device port

    Returns:
        Dictionary with test results
    """
    result = {
        'success': False,
        'message': '',
        'device_info': None,
        'error': None
    }

    try:
        manager = ZKDeviceManager(ip, port)

        if manager.connect():
            result['success'] = True
            result['message'] = f'Successfully connected to device at {ip}:{port}'
            result['device_info'] = manager.get_device_info()
            manager.disconnect()
        else:
            result['message'] = f'Failed to connect to device at {ip}:{port}'
            result['error'] = 'Connection failed'

    except Exception as e:
        result['message'] = f'Error testing connection: {str(e)}'
        result['error'] = str(e)

    return result


def get_sync_status() -> Dict[str, any]:
    """
    Get current sync status and statistics
    الحصول على حالة المزامنة الحالية والإحصائيات

    Returns:
        Dictionary with sync status
    """
    status = {
        'unprocessed_logs': 0,
        'last_sync_time': None,
        'devices_configured': 0,
        'recent_attendance': []
    }

    try:
        # Count unprocessed logs
        status['unprocessed_logs'] = AttendanceLog.objects.filter(is_processed=False).count()

        # Get last sync time
        last_log = AttendanceLog.objects.order_by('-created_at').first()
        if last_log:
            status['last_sync_time'] = last_log.created_at

        # Count configured devices
        devices = get_configured_devices()
        status['devices_configured'] = len(devices)

        # Get recent attendance records
        recent = Attendance.objects.order_by('-date', '-created_at')[:10]
        status['recent_attendance'] = [
            {
                'employee': att.employee.emp_code,
                'date': att.date,
                'check_in': att.check_in,
                'check_out': att.check_out,
                'status': att.status
            }
            for att in recent
        ]

    except Exception as e:
        logger.error(f"Error getting sync status: {str(e)}")

    return status

