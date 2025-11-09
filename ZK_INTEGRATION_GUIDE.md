# دليل تكامل أجهزة البصمة ZK
# ZK Fingerprint Device Integration Guide

## نظرة عامة | Overview

This guide explains how to use the enhanced ZK fingerprint device integration system in the HR Management System.

يشرح هذا الدليل كيفية استخدام نظام تكامل أجهزة البصمة ZK المحسّن في نظام إدارة الموارد البشرية.

---

## المميزات | Features

### ✅ Enhanced Features

1. **Robust Error Handling** - معالجة محسّنة للأخطاء
   - Automatic retry logic with configurable attempts
   - Comprehensive error logging
   - Graceful failure handling

2. **Data Validation** - التحقق من صحة البيانات
   - Timestamp validation (not in future, not too old)
   - Employee status verification
   - Duplicate record detection

3. **Intelligent Punch Type Detection** - كشف ذكي لنوع التسجيل
   - Device-based detection (if supported)
   - Context-based detection (based on previous logs)
   - Time-based fallback

4. **Automatic Synchronization** - المزامنة التلقائية
   - Celery-based scheduled tasks
   - Configurable sync intervals
   - Auto-processing of logs

5. **Comprehensive Logging** - تسجيل شامل
   - Detailed operation logs
   - Error tracking
   - Performance monitoring

6. **User-Friendly Management** - إدارة سهلة الاستخدام
   - Django management commands
   - Device connection testing
   - Sync status monitoring

---

## التثبيت والإعداد | Installation & Setup

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Configure Redis (for Celery)

Install and start Redis server:

```bash
# Windows (using Chocolatey)
choco install redis-64

# Or download from: https://github.com/microsoftarchive/redis/releases

# Start Redis
redis-server
```

### 3. Configure ZK Devices

Add device configuration in Django admin or database:

**Model:** `SystemSettings`
- **Key:** `zk_devices`
- **Value:** `Device1|192.168.1.100:4370,Device2|192.168.1.101:4370`

**Format:** `name|ip:port,name|ip:port,...`

Example:
```
Main Entrance|192.168.1.100:4370,Back Door|192.168.1.101:4370
```

### 4. Configure Employee ZK User IDs

For each employee, set the `zk_user_id` field to match their ID on the ZK device.

### 5. Create Logs Directory

```bash
mkdir logs
```

---

## الاستخدام | Usage

### Method 1: Django Management Command (Recommended)

#### List Configured Devices
```bash
python manage.py sync_zk_devices --list-devices
```

#### Test All Devices
```bash
python manage.py sync_zk_devices --test
```

#### Test Specific Device
```bash
python manage.py sync_zk_devices --device 192.168.1.100:4370
```

#### Check Sync Status
```bash
python manage.py sync_zk_devices --status
```

#### Sync All Devices
```bash
# Sync all records
python manage.py sync_zk_devices

# Sync last 7 days
python manage.py sync_zk_devices --days 7

# Sync without auto-processing
python manage.py sync_zk_devices --no-process
```

### Method 2: Python Code

```python
from attendance.zk_integration import (
    sync_all_devices,
    test_device_connection,
    get_sync_status,
    ZKDeviceManager
)

# Test device connection
result = test_device_connection('192.168.1.100', 4370)
print(result)

# Sync all devices
results = sync_all_devices(auto_process=True)
print(f"Synced {results['total_success']} records")

# Get sync status
status = get_sync_status()
print(f"Unprocessed logs: {status['unprocessed_logs']}")

# Work with specific device
manager = ZKDeviceManager('192.168.1.100', 4370, 'Main Entrance')
if manager.connect():
    # Get device info
    info = manager.get_device_info()
    print(info)
    
    # Sync attendance
    stats = manager.sync_attendance_logs()
    print(stats)
    
    # Process logs
    process_stats = manager.process_attendance_logs()
    print(process_stats)
```

### Method 3: Celery Tasks (Automatic)

#### Start Celery Worker
```bash
celery -A HR_sys worker -l info
```

#### Start Celery Beat (Scheduler)
```bash
celery -A HR_sys beat -l info
```

#### Run Both Together
```bash
celery -A HR_sys worker -B -l info
```

**Scheduled Tasks:**
- Sync devices every 30 minutes
- Process logs every 15 minutes
- Calculate daily attendance at 11:00 PM
- Send late notifications at 9:30 AM

---

## سير العمل | Workflow

### 1. Data Flow

```
ZK Device → AttendanceLog (raw) → Attendance (processed)
```

1. **Sync:** Fetch raw logs from ZK devices → Save to `AttendanceLog`
2. **Process:** Group logs by employee/date → Create/Update `Attendance` records
3. **Calculate:** Compute work hours, late minutes, overtime, etc.

### 2. Sync Process

```python
# Step 1: Connect to device
manager.connect()

# Step 2: Fetch attendance logs
logs = manager.get_attendance_logs()

# Step 3: Validate and save each log
for log in logs:
    validate_attendance_record(log, employee)
    AttendanceLog.objects.create(...)

# Step 4: Disconnect
manager.disconnect()
```

### 3. Processing Logic

```python
# Group logs by employee and date
logs_by_employee_date = group_logs(unprocessed_logs)

# For each group:
for (employee, date), logs in logs_by_employee_date.items():
    # Find earliest check-in
    check_in = min(check_in_logs)
    
    # Find latest check-out
    check_out = max(check_out_logs)
    
    # Calculate work hours
    work_hours = (check_out - check_in) - break_time
    
    # Calculate late minutes
    if check_in > expected_time:
        late_minutes = (check_in - expected_time).minutes
    
    # Save attendance record
    Attendance.objects.create(...)
```

---

## استكشاف الأخطاء | Troubleshooting

### Problem: Cannot connect to device

**Solutions:**
1. Check device IP and port
2. Ensure device is powered on and connected to network
3. Check firewall settings
4. Verify network connectivity: `ping 192.168.1.100`

### Problem: Employee not found

**Solutions:**
1. Ensure employee has `zk_user_id` set
2. Verify `zk_user_id` matches device user ID
3. Check employee `is_active` status

### Problem: Duplicate records

**Solution:**
- The system automatically handles duplicates
- Duplicate logs are skipped and counted in stats

### Problem: Incorrect punch type

**Solutions:**
1. Check if device provides punch state
2. Review `_determine_punch_type` logic
3. Manually correct in admin if needed

### Problem: Celery tasks not running

**Solutions:**
1. Ensure Redis is running: `redis-cli ping`
2. Check Celery worker is running
3. Check Celery beat is running
4. Review logs: `logs/hr_sys.log`

---

## الإعدادات المتقدمة | Advanced Configuration

### Custom Sync Schedule

Edit `HR_sys/celery.py`:

```python
app.conf.beat_schedule = {
    'sync-zk-devices-custom': {
        'task': 'attendance.sync_zk_devices',
        'schedule': crontab(hour='*/2'),  # Every 2 hours
        'args': (7, True),  # Sync last 7 days
    },
}
```

### Connection Settings

Edit `attendance/zk_integration.py`:

```python
class ZKDeviceManager:
    MAX_RETRIES = 5  # Increase retry attempts
    RETRY_DELAY = 3  # Increase delay between retries
    CONNECTION_TIMEOUT = 15  # Increase timeout
```

### Validation Rules

Edit `validate_attendance_record` method:

```python
def validate_attendance_record(self, record, employee):
    # Add custom validation rules
    if record.timestamp.hour > 23:
        return False, "Invalid hour"
    
    # ... more rules
```

---

## واجهة برمجة التطبيقات | API Reference

### ZKDeviceManager Class

#### Methods:

- `connect(retry=True)` - Connect to device
- `disconnect()` - Disconnect from device
- `is_connected()` - Check connection status
- `get_device_info()` - Get device information
- `get_attendance_logs(start_date, end_date)` - Fetch logs
- `sync_attendance_logs(start_date, end_date)` - Sync logs to database
- `process_attendance_logs(employee_id, date)` - Process unprocessed logs
- `get_users()` - Get all users from device
- `add_user(user_id, name, ...)` - Add user to device
- `delete_user(user_id)` - Delete user from device
- `sync_employee_to_device(employee)` - Sync employee to device
- `clear_attendance_logs()` - Clear all logs from device

### Utility Functions:

- `get_configured_devices()` - Get list of configured devices
- `sync_all_devices(start_date, end_date, auto_process)` - Sync all devices
- `test_device_connection(ip, port)` - Test device connection
- `get_sync_status()` - Get current sync status

### Celery Tasks:

- `sync_zk_devices_task(days, auto_process)` - Sync devices task
- `process_attendance_logs_task(employee_id, date)` - Process logs task
- `calculate_daily_attendance_task(date)` - Calculate daily attendance
- `send_late_notifications_task(date)` - Send late notifications

---

## الأمان | Security

### Best Practices:

1. **Network Security:**
   - Use VPN for remote device access
   - Configure firewall rules
   - Use static IPs for devices

2. **Data Security:**
   - Regular database backups
   - Encrypt sensitive data
   - Audit log access

3. **Access Control:**
   - Limit admin access
   - Use role-based permissions
   - Monitor system logs

---

## الأداء | Performance

### Optimization Tips:

1. **Sync Frequency:**
   - Don't sync too frequently (recommended: 30 minutes)
   - Use date filtering for large datasets

2. **Processing:**
   - Process logs in batches
   - Use database indexing
   - Clean old logs periodically

3. **Monitoring:**
   - Monitor Celery queue length
   - Check Redis memory usage
   - Review log file sizes

---

## الدعم | Support

For issues or questions:

1. Check logs: `logs/hr_sys.log`
2. Review Django admin: `/admin/`
3. Test device connection
4. Check Celery worker status

---

## التحديثات المستقبلية | Future Enhancements

Planned features:

- [ ] Web-based device management interface
- [ ] Real-time sync monitoring dashboard
- [ ] Mobile app integration
- [ ] Biometric data backup
- [ ] Multi-language device support
- [ ] Advanced reporting and analytics

---

**Version:** 1.0  
**Last Updated:** 2025-11-09  
**Author:** HR System Development Team

