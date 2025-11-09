"""
Performance management models
"""
from django.db import models
from core.models import BaseModel


class PerformanceReviewCycle(BaseModel):
    """
    Performance review cycles
    دورات تقييم الأداء
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم الدورة'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        verbose_name='تاريخ النهاية'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط'
    )
    
    class Meta:
        db_table = 'Tbl_Performance_Review_Cycles'
        verbose_name = 'دورة تقييم أداء'
        verbose_name_plural = 'دورات تقييم الأداء'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class PerformanceReview(BaseModel):
    """
    Employee performance reviews
    تقييمات أداء الموظفين
    """
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('submitted', 'مقدم'),
        ('approved', 'معتمد'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='performance_reviews',
        verbose_name='الموظف'
    )
    review_cycle = models.ForeignKey(
        PerformanceReviewCycle,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='دورة التقييم'
    )
    reviewer = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='conducted_reviews',
        verbose_name='المقيّم'
    )
    review_date = models.DateField(
        verbose_name='تاريخ التقييم'
    )
    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name='التقييم الإجمالي'
    )
    strengths = models.TextField(
        blank=True,
        null=True,
        verbose_name='نقاط القوة'
    )
    weaknesses = models.TextField(
        blank=True,
        null=True,
        verbose_name='نقاط الضعف'
    )
    recommendations = models.TextField(
        blank=True,
        null=True,
        verbose_name='التوصيات'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='الحالة'
    )
    
    class Meta:
        db_table = 'Tbl_Performance_Reviews'
        verbose_name = 'تقييم أداء'
        verbose_name_plural = 'تقييمات الأداء'
        ordering = ['-review_date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.review_cycle.name}"


class KPI(BaseModel):
    """
    Key Performance Indicators
    مؤشرات الأداء الرئيسية
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم المؤشر'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='وحدة القياس'
    )
    target_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='القيمة المستهدفة'
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='الوزن النسبي'
    )
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='القسم'
    )
    
    class Meta:
        db_table = 'Tbl_KPIs'
        verbose_name = 'مؤشر أداء'
        verbose_name_plural = 'مؤشرات الأداء'
    
    def __str__(self):
        return self.name


class EmployeeKPI(BaseModel):
    """
    Employee KPI assignments and tracking
    تعيين وتتبع مؤشرات أداء الموظفين
    """
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='kpis',
        verbose_name='الموظف'
    )
    kpi = models.ForeignKey(
        KPI,
        on_delete=models.CASCADE,
        verbose_name='مؤشر الأداء'
    )
    review_cycle = models.ForeignKey(
        PerformanceReviewCycle,
        on_delete=models.CASCADE,
        verbose_name='دورة التقييم'
    )
    target_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='القيمة المستهدفة'
    )
    actual_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='القيمة الفعلية'
    )
    achievement_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='نسبة الإنجاز'
    )
    
    class Meta:
        db_table = 'Tbl_Employee_KPIs'
        verbose_name = 'مؤشر أداء موظف'
        verbose_name_plural = 'مؤشرات أداء الموظفين'
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.kpi.name}"
    
    def calculate_achievement(self):
        """Calculate achievement percentage"""
        if self.actual_value and self.target_value:
            self.achievement_percentage = (self.actual_value / self.target_value) * 100
            return self.achievement_percentage
        return 0


class Goal(BaseModel):
    """
    Employee goals
    أهداف الموظفين
    """
    STATUS_CHOICES = [
        ('not_started', 'لم يبدأ'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name='الموظف'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='العنوان'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    due_date = models.DateField(
        verbose_name='تاريخ الاستحقاق'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started',
        verbose_name='الحالة'
    )
    progress = models.IntegerField(
        default=0,
        verbose_name='التقدم (%)'
    )
    
    class Meta:
        db_table = 'Tbl_Goals'
        verbose_name = 'هدف'
        verbose_name_plural = 'الأهداف'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.title}"

