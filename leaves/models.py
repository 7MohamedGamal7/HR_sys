"""
Leave management models
"""
from django.db import models
from core.models import BaseModel


class LeavePolicy(BaseModel):
    """
    Leave policies for different leave types
    سياسات الإجازات
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم السياسة'
    )
    leave_type = models.CharField(
        max_length=50,
        verbose_name='نوع الإجازة'
    )
    days_per_year = models.IntegerField(
        verbose_name='الأيام في السنة'
    )
    max_consecutive_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='الحد الأقصى للأيام المتتالية'
    )
    requires_approval = models.BooleanField(
        default=True,
        verbose_name='تتطلب موافقة'
    )
    is_paid = models.BooleanField(
        default=True,
        verbose_name='مدفوعة'
    )
    carry_forward = models.BooleanField(
        default=False,
        verbose_name='يمكن ترحيلها'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    
    class Meta:
        db_table = 'Tbl_Leave_Policies'
        verbose_name = 'سياسة إجازة'
        verbose_name_plural = 'سياسات الإجازات'
    
    def __str__(self):
        return self.name


class LeaveBalance(BaseModel):
    """
    Employee leave balances
    أرصدة إجازات الموظفين
    """
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances',
        verbose_name='الموظف'
    )
    leave_type = models.CharField(
        max_length=50,
        verbose_name='نوع الإجازة'
    )
    year = models.IntegerField(
        verbose_name='السنة'
    )
    total_days = models.IntegerField(
        verbose_name='إجمالي الأيام'
    )
    used_days = models.IntegerField(
        default=0,
        verbose_name='الأيام المستخدمة'
    )
    remaining_days = models.IntegerField(
        verbose_name='الأيام المتبقية'
    )
    
    class Meta:
        db_table = 'Tbl_Leave_Balances'
        verbose_name = 'رصيد إجازة'
        verbose_name_plural = 'أرصدة الإجازات'
        unique_together = ['employee', 'leave_type', 'year']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.leave_type} ({self.year})"
    
    def save(self, *args, **kwargs):
        self.remaining_days = self.total_days - self.used_days
        super().save(*args, **kwargs)


class LeaveApprovalWorkflow(BaseModel):
    """
    Leave approval workflow
    سير عمل الموافقة على الإجازات
    """
    leave_request = models.ForeignKey(
        'attendance.LeaveRequest',
        on_delete=models.CASCADE,
        related_name='approval_workflow',
        verbose_name='طلب الإجازة'
    )
    approver = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        verbose_name='المعتمد'
    )
    level = models.IntegerField(
        verbose_name='المستوى'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'قيد الانتظار'),
            ('approved', 'موافق'),
            ('rejected', 'مرفوض'),
        ],
        default='pending',
        verbose_name='الحالة'
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='التعليقات'
    )
    action_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ الإجراء'
    )
    
    class Meta:
        db_table = 'Tbl_Leave_Approval_Workflow'
        verbose_name = 'سير عمل الموافقة'
        verbose_name_plural = 'سير عمل الموافقات'
        ordering = ['level']
    
    def __str__(self):
        return f"{self.leave_request} - Level {self.level}"

