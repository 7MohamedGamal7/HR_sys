"""
Recruitment and onboarding models
"""
from django.db import models
from core.models import BaseModel


class JobPosting(BaseModel):
    """
    Job postings
    الإعلانات الوظيفية
    """
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('published', 'منشور'),
        ('closed', 'مغلق'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='المسمى الوظيفي'
    )
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='القسم'
    )
    position = models.ForeignKey(
        'organization.Position',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='المنصب'
    )
    description = models.TextField(
        verbose_name='الوصف الوظيفي'
    )
    requirements = models.TextField(
        verbose_name='المتطلبات'
    )
    responsibilities = models.TextField(
        verbose_name='المسؤوليات'
    )
    salary_range_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الحد الأدنى للراتب'
    )
    salary_range_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الحد الأقصى للراتب'
    )
    vacancies = models.IntegerField(
        default=1,
        verbose_name='عدد الشواغر'
    )
    posting_date = models.DateField(
        verbose_name='تاريخ النشر'
    )
    closing_date = models.DateField(
        verbose_name='تاريخ الإغلاق'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='الحالة'
    )
    
    class Meta:
        db_table = 'Tbl_Job_Postings'
        verbose_name = 'إعلان وظيفي'
        verbose_name_plural = 'الإعلانات الوظيفية'
        ordering = ['-posting_date']
    
    def __str__(self):
        return self.title


class JobApplication(BaseModel):
    """
    Job applications
    طلبات التوظيف
    """
    STATUS_CHOICES = [
        ('received', 'مستلم'),
        ('screening', 'فحص أولي'),
        ('interview', 'مقابلة'),
        ('offer', 'عرض'),
        ('hired', 'تم التوظيف'),
        ('rejected', 'مرفوض'),
    ]
    
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='الإعلان الوظيفي'
    )
    applicant_name = models.CharField(
        max_length=200,
        verbose_name='اسم المتقدم'
    )
    email = models.EmailField(
        verbose_name='البريد الإلكتروني'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف'
    )
    resume = models.FileField(
        upload_to='recruitment/resumes/',
        verbose_name='السيرة الذاتية'
    )
    cover_letter = models.TextField(
        blank=True,
        null=True,
        verbose_name='خطاب التقديم'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received',
        verbose_name='الحالة'
    )
    application_date = models.DateField(
        auto_now_add=True,
        verbose_name='تاريخ التقديم'
    )
    
    class Meta:
        db_table = 'Tbl_Job_Applications'
        verbose_name = 'طلب توظيف'
        verbose_name_plural = 'طلبات التوظيف'
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.applicant_name} - {self.job_posting.title}"


class Interview(BaseModel):
    """
    Interview scheduling and tracking
    جدولة وتتبع المقابلات
    """
    STATUS_CHOICES = [
        ('scheduled', 'مجدولة'),
        ('completed', 'مكتملة'),
        ('cancelled', 'ملغاة'),
    ]
    
    RESULT_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('passed', 'ناجح'),
        ('failed', 'راسب'),
    ]
    
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='interviews',
        verbose_name='طلب التوظيف'
    )
    interview_date = models.DateTimeField(
        verbose_name='تاريخ ووقت المقابلة'
    )
    interviewer = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='المقابل'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='المكان'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name='الحالة'
    )
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='pending',
        verbose_name='النتيجة'
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name='الملاحظات'
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='التقييم (1-10)'
    )
    
    class Meta:
        db_table = 'Tbl_Interviews'
        verbose_name = 'مقابلة'
        verbose_name_plural = 'المقابلات'
        ordering = ['-interview_date']
    
    def __str__(self):
        return f"{self.application.applicant_name} - {self.interview_date}"


class OnboardingTask(BaseModel):
    """
    Onboarding tasks for new employees
    مهام التأهيل للموظفين الجدد
    """
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='onboarding_tasks',
        verbose_name='الموظف'
    )
    task_name = models.CharField(
        max_length=200,
        verbose_name='اسم المهمة'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    assigned_to = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='مسند إلى'
    )
    due_date = models.DateField(
        verbose_name='تاريخ الاستحقاق'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )
    completed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الإكمال'
    )
    
    class Meta:
        db_table = 'Tbl_Onboarding_Tasks'
        verbose_name = 'مهمة تأهيل'
        verbose_name_plural = 'مهام التأهيل'
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.task_name}"

