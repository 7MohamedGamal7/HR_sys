"""
Training and development models
"""
from django.db import models
from core.models import BaseModel


class TrainingProgram(BaseModel):
    """
    Training programs
    البرامج التدريبية
    """
    STATUS_CHOICES = [
        ('planned', 'مخطط'),
        ('ongoing', 'جاري'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='اسم البرنامج'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    objectives = models.TextField(
        verbose_name='الأهداف'
    )
    duration_hours = models.IntegerField(
        verbose_name='المدة (ساعات)'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        verbose_name='تاريخ النهاية'
    )
    trainer = models.CharField(
        max_length=200,
        verbose_name='المدرب'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='المكان'
    )
    max_participants = models.IntegerField(
        verbose_name='الحد الأقصى للمشاركين'
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='التكلفة'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name='الحالة'
    )
    
    class Meta:
        db_table = 'Tbl_Training_Programs'
        verbose_name = 'برنامج تدريبي'
        verbose_name_plural = 'البرامج التدريبية'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class TrainingEnrollment(BaseModel):
    """
    Employee training enrollments
    تسجيلات الموظفين في التدريب
    """
    STATUS_CHOICES = [
        ('registered', 'مسجل'),
        ('attended', 'حضر'),
        ('completed', 'أكمل'),
        ('failed', 'راسب'),
        ('cancelled', 'ملغى'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='training_enrollments',
        verbose_name='الموظف'
    )
    training_program = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='البرنامج التدريبي'
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name='تاريخ التسجيل'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered',
        verbose_name='الحالة'
    )
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='نسبة الحضور'
    )
    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='الدرجة النهائية'
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name='الملاحظات'
    )
    certificate_issued = models.BooleanField(
        default=False,
        verbose_name='تم إصدار الشهادة'
    )
    
    class Meta:
        db_table = 'Tbl_Training_Enrollments'
        verbose_name = 'تسجيل تدريبي'
        verbose_name_plural = 'التسجيلات التدريبية'
        unique_together = ['employee', 'training_program']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.training_program.name}"


class TrainingCertificate(BaseModel):
    """
    Training certificates
    شهادات التدريب
    """
    enrollment = models.OneToOneField(
        TrainingEnrollment,
        on_delete=models.CASCADE,
        related_name='certificate',
        verbose_name='التسجيل التدريبي'
    )
    certificate_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='رقم الشهادة'
    )
    issue_date = models.DateField(
        verbose_name='تاريخ الإصدار'
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الانتهاء'
    )
    certificate_file = models.FileField(
        upload_to='training/certificates/',
        blank=True,
        null=True,
        verbose_name='ملف الشهادة'
    )
    
    class Meta:
        db_table = 'Tbl_Training_Certificates'
        verbose_name = 'شهادة تدريب'
        verbose_name_plural = 'شهادات التدريب'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.certificate_number} - {self.enrollment.employee.emp_code}"


class SkillCategory(BaseModel):
    """
    Skill categories
    فئات المهارات
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم الفئة'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    
    class Meta:
        db_table = 'Tbl_Skill_Categories'
        verbose_name = 'فئة مهارة'
        verbose_name_plural = 'فئات المهارات'
    
    def __str__(self):
        return self.name


class Skill(BaseModel):
    """
    Skills
    المهارات
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم المهارة'
    )
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='الفئة'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    
    class Meta:
        db_table = 'Tbl_Skills'
        verbose_name = 'مهارة'
        verbose_name_plural = 'المهارات'
    
    def __str__(self):
        return self.name


class EmployeeSkill(BaseModel):
    """
    Employee skills and proficiency levels
    مهارات الموظفين ومستويات الكفاءة
    """
    PROFICIENCY_LEVELS = [
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
        ('expert', 'خبير'),
    ]
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='الموظف'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='المهارة'
    )
    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_LEVELS,
        verbose_name='مستوى الكفاءة'
    )
    years_of_experience = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='سنوات الخبرة'
    )
    last_used_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ آخر استخدام'
    )
    
    class Meta:
        db_table = 'Tbl_Employee_Skills'
        verbose_name = 'مهارة موظف'
        verbose_name_plural = 'مهارات الموظفين'
        unique_together = ['employee', 'skill']
    
    def __str__(self):
        return f"{self.employee.emp_code} - {self.skill.name}"

