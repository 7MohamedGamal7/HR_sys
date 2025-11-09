"""
Attendance models for time tracking and ZK device integration
"""
from django.db import models
from core.models import BaseModel
from django.utils import timezone


class Attendance(BaseModel):
    """
    Daily attendance records
    سجلات الحضور اليومية
    """
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غائب'),
        ('late', 'متأخر'),
        ('half_day', 'نصف يوم'),
        ('on_leave', 'في إجازة'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='الموظف'
    )
    date = models.DateField(
        verbose_name='التاريخ'
    )
    check_in = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='وقت الحضور'
    )
    check_out = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='وقت الانصراف'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present',
        verbose_name='الحالة'
    )
    work_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='ساعات العمل'
    )
    late_minutes = models.IntegerField(
        default=0,
        verbose_name='دقائق التأخير'
    )
    early_leave_minutes = models.IntegerField(
        default=0,
        verbose_name='دقائق المغادرة المبكرة'
    )
    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='ساعات العمل الإضافي'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )
    
    class Meta:
        db_table = 'Tbl_Attendance_New'
        verbose_name = 'سجل حضور'
        verbose_name_plural = 'سجلات الحضور'
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.date}"
    
    def calculate_work_hours(self):
        """Calculate work hours from check-in and check-out"""
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            hours = delta.total_seconds() / 3600
            # Subtract break time if applicable
            if self.employee.work_shift:
                hours -= (self.employee.work_shift.break_duration / 60)
            self.work_hours = round(hours, 2)
            return self.work_hours
        return 0


class AttendanceLog(models.Model):
    """
    Raw attendance logs from ZK device
    سجلات الحضور الخام من جهاز البصمة
    """
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='attendance_logs',
        verbose_name='الموظف'
    )
    timestamp = models.DateTimeField(
        verbose_name='الوقت'
    )
    device_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='معرف الجهاز'
    )
    punch_type = models.CharField(
        max_length=20,
        choices=[
            ('check_in', 'حضور'),
            ('check_out', 'انصراف'),
            ('break_out', 'بداية استراحة'),
            ('break_in', 'نهاية استراحة'),
        ],
        default='check_in',
        verbose_name='نوع التسجيل'
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name='تمت المعالجة'
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='وقت المعالجة'
    )
    
    class Meta:
        db_table = 'Tbl_Attendance_Logs'
        verbose_name = 'سجل بصمة'
        verbose_name_plural = 'سجلات البصمة'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.timestamp}"


class LeaveRequest(BaseModel):
    """
    Leave requests (moved from leaves app for better organization)
    طلبات الإجازات
    """
    LEAVE_TYPES = [
        ('annual', 'إجازة سنوية'),
        ('sick', 'إجازة مرضية'),
        ('emergency', 'إجازة طارئة'),
        ('unpaid', 'إجازة بدون راتب'),
        ('maternity', 'إجازة أمومة'),
        ('paternity', 'إجازة أبوة'),
        ('hajj', 'إجازة حج'),
        ('other', 'أخرى'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('approved', 'موافق عليها'),
        ('rejected', 'مرفوضة'),
        ('cancelled', 'ملغاة'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_requests',
        verbose_name='الموظف'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES,
        verbose_name='نوع الإجازة'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        verbose_name='تاريخ النهاية'
    )
    days_count = models.IntegerField(
        verbose_name='عدد الأيام'
    )
    reason = models.TextField(
        verbose_name='السبب'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )
    approved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves',
        verbose_name='تمت الموافقة بواسطة'
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='وقت الموافقة'
    )
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='سبب الرفض'
    )
    attachment = models.FileField(
        upload_to='leaves/attachments/',
        blank=True,
        null=True,
        verbose_name='مرفق'
    )
    
    class Meta:
        db_table = 'Tbl_Leave_Requests'
        verbose_name = 'طلب إجازة'
        verbose_name_plural = 'طلبات الإجازات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        """Calculate days count before saving"""
        if self.start_date and self.end_date:
            from core.utils import calculate_working_days
            self.days_count = calculate_working_days(self.start_date, self.end_date)
        super().save(*args, **kwargs)


class Overtime(BaseModel):
    """
    Overtime records
    سجلات العمل الإضافي
    """
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('approved', 'موافق عليه'),
        ('rejected', 'مرفوض'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='overtime_records',
        verbose_name='الموظف'
    )
    date = models.DateField(
        verbose_name='التاريخ'
    )
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='عدد الساعات'
    )
    reason = models.TextField(
        verbose_name='السبب'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )
    approved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_overtime',
        verbose_name='تمت الموافقة بواسطة'
    )
    
    class Meta:
        db_table = 'Tbl_Overtime'
        verbose_name = 'عمل إضافي'
        verbose_name_plural = 'العمل الإضافي'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.date} ({self.hours} hours)"

