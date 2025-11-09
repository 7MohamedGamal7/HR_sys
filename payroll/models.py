"""
Payroll management models
"""
from django.db import models
from core.models import BaseModel
from decimal import Decimal


class Payroll(BaseModel):
    """
    Monthly payroll records
    سجلات الرواتب الشهرية
    """
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('processing', 'قيد المعالجة'),
        ('approved', 'معتمد'),
        ('paid', 'مدفوع'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='payrolls',
        verbose_name='الموظف'
    )
    month = models.IntegerField(
        verbose_name='الشهر'
    )
    year = models.IntegerField(
        verbose_name='السنة'
    )
    
    # Earnings
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='الراتب الأساسي'
    )
    housing_allowance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='بدل السكن'
    )
    transport_allowance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='بدل النقل'
    )
    other_allowances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='بدلات أخرى'
    )
    overtime_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='مبلغ العمل الإضافي'
    )
    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='المكافأة'
    )
    
    # Deductions
    absence_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصم الغياب'
    )
    late_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصم التأخير'
    )
    loan_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصم القرض'
    )
    insurance_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصم التأمين'
    )
    tax_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصم الضريبة'
    )
    other_deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='خصومات أخرى'
    )
    
    # Totals
    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='إجمالي الراتب'
    )
    total_deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='إجمالي الخصومات'
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='صافي الراتب'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='الحالة'
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الدفع'
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='طريقة الدفع'
    )
    
    class Meta:
        db_table = 'Tbl_Payrolls'
        verbose_name = 'راتب'
        verbose_name_plural = 'الرواتب'
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.month}/{self.year}"
    
    def calculate_totals(self):
        """Calculate gross, total deductions, and net salary"""
        self.gross_salary = (
            self.basic_salary + self.housing_allowance + 
            self.transport_allowance + self.other_allowances +
            self.overtime_amount + self.bonus
        )
        
        self.total_deductions = (
            self.absence_deduction + self.late_deduction +
            self.loan_deduction + self.insurance_deduction +
            self.tax_deduction + self.other_deductions
        )
        
        self.net_salary = self.gross_salary - self.total_deductions
    
    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)


class Payslip(BaseModel):
    """
    Payslip documents
    قسائم الرواتب
    """
    payroll = models.OneToOneField(
        Payroll,
        on_delete=models.CASCADE,
        related_name='payslip',
        verbose_name='الراتب'
    )
    payslip_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='رقم القسيمة'
    )
    generated_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    pdf_file = models.FileField(
        upload_to='payslips/',
        blank=True,
        null=True,
        verbose_name='ملف PDF'
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name='تم الإرسال'
    )
    sent_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ الإرسال'
    )
    
    class Meta:
        db_table = 'Tbl_Payslips'
        verbose_name = 'قسيمة راتب'
        verbose_name_plural = 'قسائم الرواتب'
        ordering = ['-generated_date']
    
    def __str__(self):
        return f"{self.payslip_number} - {self.payroll.employee.emp_code}"


class Loan(BaseModel):
    """
    Employee loans
    قروض الموظفين
    """
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
        ('active', 'نشط'),
        ('completed', 'مكتمل'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name='الموظف'
    )
    loan_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='مبلغ القرض'
    )
    installment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='مبلغ القسط'
    )
    number_of_installments = models.IntegerField(
        verbose_name='عدد الأقساط'
    )
    paid_installments = models.IntegerField(
        default=0,
        verbose_name='الأقساط المدفوعة'
    )
    remaining_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='المبلغ المتبقي'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        verbose_name='تاريخ النهاية'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )
    reason = models.TextField(
        verbose_name='السبب'
    )
    approved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='تمت الموافقة بواسطة'
    )
    
    class Meta:
        db_table = 'Tbl_Loans'
        verbose_name = 'قرض'
        verbose_name_plural = 'القروض'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.loan_amount}"
    
    def save(self, *args, **kwargs):
        self.remaining_amount = self.loan_amount - (self.paid_installments * self.installment_amount)
        super().save(*args, **kwargs)


class Bonus(BaseModel):
    """
    Employee bonuses
    مكافآت الموظفين
    """
    BONUS_TYPES = [
        ('performance', 'أداء'),
        ('annual', 'سنوية'),
        ('project', 'مشروع'),
        ('other', 'أخرى'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='bonuses',
        verbose_name='الموظف'
    )
    bonus_type = models.CharField(
        max_length=20,
        choices=BONUS_TYPES,
        verbose_name='نوع المكافأة'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='المبلغ'
    )
    date = models.DateField(
        verbose_name='التاريخ'
    )
    reason = models.TextField(
        verbose_name='السبب'
    )
    approved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='تمت الموافقة بواسطة'
    )
    
    class Meta:
        db_table = 'Tbl_Bonuses'
        verbose_name = 'مكافأة'
        verbose_name_plural = 'المكافآت'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.amount}"

