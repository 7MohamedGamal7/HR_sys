"""
Organization models for departments, positions, and organizational structure
"""
from django.db import models
from core.models import BaseModel


class Department(BaseModel):
    """
    Department model
    نموذج القسم
    """
    dept_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رمز القسم'
    )
    dept_name_ar = models.CharField(
        max_length=200,
        verbose_name='اسم القسم بالعربية'
    )
    dept_name_en = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='اسم القسم بالإنجليزية'
    )
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments',
        verbose_name='القسم الأب'
    )
    manager = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name='مدير القسم'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الميزانية'
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='الموقع'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='الهاتف'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='البريد الإلكتروني'
    )
    
    class Meta:
        db_table = 'Tbl_Departments'
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'
        ordering = ['dept_code']
    
    def __str__(self):
        return self.dept_name_ar
    
    def get_all_employees(self):
        """Get all employees in this department including sub-departments"""
        from employees.models import Employee
        employees = Employee.objects.filter(department=self)
        for sub_dept in self.sub_departments.all():
            employees |= sub_dept.get_all_employees()
        return employees
    
    def get_employee_count(self):
        """Get count of employees in this department"""
        return self.employees.filter(is_active=True).count()


class Position(BaseModel):
    """
    Position/Job Title model
    نموذج المنصب/المسمى الوظيفي
    """
    position_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رمز المنصب'
    )
    position_name_ar = models.CharField(
        max_length=200,
        verbose_name='اسم المنصب بالعربية'
    )
    position_name_en = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='اسم المنصب بالإنجليزية'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='positions',
        verbose_name='القسم'
    )
    level = models.IntegerField(
        default=1,
        verbose_name='المستوى'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    responsibilities = models.TextField(
        blank=True,
        null=True,
        verbose_name='المسؤوليات'
    )
    requirements = models.TextField(
        blank=True,
        null=True,
        verbose_name='المتطلبات'
    )
    min_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الحد الأدنى للراتب'
    )
    max_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الحد الأقصى للراتب'
    )
    
    class Meta:
        db_table = 'Tbl_Positions'
        verbose_name = 'منصب'
        verbose_name_plural = 'المناصب'
        ordering = ['level', 'position_name_ar']
    
    def __str__(self):
        return self.position_name_ar


class Branch(BaseModel):
    """
    Branch/Office model
    نموذج الفرع/المكتب
    """
    branch_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رمز الفرع'
    )
    branch_name_ar = models.CharField(
        max_length=200,
        verbose_name='اسم الفرع بالعربية'
    )
    branch_name_en = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='اسم الفرع بالإنجليزية'
    )
    address = models.TextField(
        verbose_name='العنوان'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='المدينة'
    )
    country = models.CharField(
        max_length=100,
        default='المملكة العربية السعودية',
        verbose_name='الدولة'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='الهاتف'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='البريد الإلكتروني'
    )
    manager = models.ForeignKey(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_branches',
        verbose_name='مدير الفرع'
    )
    
    class Meta:
        db_table = 'Tbl_Branches'
        verbose_name = 'فرع'
        verbose_name_plural = 'الفروع'
        ordering = ['branch_code']
    
    def __str__(self):
        return self.branch_name_ar


class WorkShift(BaseModel):
    """
    Work Shift model
    نموذج الوردية
    """
    shift_name = models.CharField(
        max_length=100,
        verbose_name='اسم الوردية'
    )
    start_time = models.TimeField(
        verbose_name='وقت البداية'
    )
    end_time = models.TimeField(
        verbose_name='وقت النهاية'
    )
    break_duration = models.IntegerField(
        default=60,
        help_text='بالدقائق',
        verbose_name='مدة الاستراحة'
    )
    working_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='ساعات العمل'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    
    class Meta:
        db_table = 'Tbl_Work_Shifts'
        verbose_name = 'وردية'
        verbose_name_plural = 'الورديات'
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.shift_name} ({self.start_time} - {self.end_time})"


class Holiday(BaseModel):
    """
    Holiday model
    نموذج العطلة الرسمية
    """
    HOLIDAY_TYPES = [
        ('national', 'عطلة وطنية'),
        ('religious', 'عطلة دينية'),
        ('other', 'أخرى'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='اسم العطلة'
    )
    date = models.DateField(
        verbose_name='التاريخ'
    )
    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPES,
        default='national',
        verbose_name='نوع العطلة'
    )
    is_recurring = models.BooleanField(
        default=False,
        verbose_name='متكررة سنوياً'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    
    class Meta:
        db_table = 'Tbl_Holidays'
        verbose_name = 'عطلة رسمية'
        verbose_name_plural = 'العطل الرسمية'
        ordering = ['date']
    
    def __str__(self):
        return f"{self.name} - {self.date}"

