"""
Reports and analytics models
"""
from django.db import models
from core.models import BaseModel


class ReportTemplate(BaseModel):
    """
    Report templates
    قوالب التقارير
    """
    REPORT_TYPES = [
        ('employee', 'تقرير الموظفين'),
        ('attendance', 'تقرير الحضور'),
        ('leave', 'تقرير الإجازات'),
        ('payroll', 'تقرير الرواتب'),
        ('performance', 'تقرير الأداء'),
        ('recruitment', 'تقرير التوظيف'),
        ('training', 'تقرير التدريب'),
        ('custom', 'تقرير مخصص'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='اسم القالب'
    )
    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPES,
        verbose_name='نوع التقرير'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    query = models.TextField(
        verbose_name='الاستعلام'
    )
    parameters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='المعاملات'
    )
    
    class Meta:
        db_table = 'Tbl_Report_Templates'
        verbose_name = 'قالب تقرير'
        verbose_name_plural = 'قوالب التقارير'
    
    def __str__(self):
        return self.name


class GeneratedReport(BaseModel):
    """
    Generated reports history
    سجل التقارير المنشأة
    """
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='القالب'
    )
    generated_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='تم الإنشاء بواسطة'
    )
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    parameters_used = models.JSONField(
        default=dict,
        verbose_name='المعاملات المستخدمة'
    )
    file_path = models.FileField(
        upload_to='reports/',
        blank=True,
        null=True,
        verbose_name='مسار الملف'
    )
    file_format = models.CharField(
        max_length=10,
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV'),
        ],
        default='pdf',
        verbose_name='صيغة الملف'
    )
    
    class Meta:
        db_table = 'Tbl_Generated_Reports'
        verbose_name = 'تقرير منشأ'
        verbose_name_plural = 'التقارير المنشأة'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.template.name if self.template else 'Unknown'} - {self.generated_at}"


class Dashboard(BaseModel):
    """
    Custom dashboards
    لوحات المعلومات المخصصة
    """
    name = models.CharField(
        max_length=200,
        verbose_name='اسم لوحة المعلومات'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    user = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='dashboards',
        verbose_name='المستخدم'
    )
    widgets = models.JSONField(
        default=list,
        verbose_name='الأدوات'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='افتراضي'
    )
    
    class Meta:
        db_table = 'Tbl_Dashboards'
        verbose_name = 'لوحة معلومات'
        verbose_name_plural = 'لوحات المعلومات'
    
    def __str__(self):
        return self.name

