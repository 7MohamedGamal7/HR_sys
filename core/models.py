"""
Core models for the HRMS system
Contains base models, custom user model, and shared utilities
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    نموذج المستخدم المخصص
    """
    ROLE_CHOICES = [
        ('admin', 'مدير النظام'),
        ('hr_manager', 'مدير الموارد البشرية'),
        ('hr_staff', 'موظف الموارد البشرية'),
        ('department_manager', 'مدير قسم'),
        ('employee', 'موظف'),
    ]
    
    employee = models.OneToOneField(
        'employees.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account',
        verbose_name='الموظف'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='الدور'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='رقم الهاتف'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='الصورة الشخصية'
    )
    is_active_user = models.BooleanField(
        default=True,
        verbose_name='نشط'
    )
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name='آخر IP للدخول'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        db_table = 'Tbl_Users'
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمون'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def has_permission(self, permission):
        """Check if user has specific permission"""
        if self.role == 'admin':
            return True
        # Add more permission logic here
        return False


class BaseModel(models.Model):
    """
    Abstract base model with common fields
    النموذج الأساسي المجرد
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='أنشئ بواسطة'
    )
    updated_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='حُدث بواسطة'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )
    
    class Meta:
        abstract = True


class SystemSettings(models.Model):
    """
    System-wide settings
    إعدادات النظام
    """
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='المفتاح'
    )
    value = models.TextField(
        verbose_name='القيمة'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )
    category = models.CharField(
        max_length=50,
        default='general',
        verbose_name='الفئة'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        db_table = 'Tbl_System_Settings'
        verbose_name = 'إعداد النظام'
        verbose_name_plural = 'إعدادات النظام'
        ordering = ['category', 'key']
    
    def __str__(self):
        return f"{self.key}: {self.value}"


class AuditLog(models.Model):
    """
    Audit log for tracking all system changes
    سجل التدقيق لتتبع جميع التغييرات
    """
    ACTION_CHOICES = [
        ('create', 'إنشاء'),
        ('update', 'تحديث'),
        ('delete', 'حذف'),
        ('login', 'تسجيل دخول'),
        ('logout', 'تسجيل خروج'),
        ('approve', 'موافقة'),
        ('reject', 'رفض'),
        ('other', 'أخرى'),
    ]
    
    user = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='المستخدم'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='الإجراء'
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name='اسم النموذج'
    )
    object_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='معرف الكائن'
    )
    description = models.TextField(
        verbose_name='الوصف'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='عنوان IP'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='الوقت'
    )
    
    class Meta:
        db_table = 'Tbl_Audit_Logs'
        verbose_name = 'سجل التدقيق'
        verbose_name_plural = 'سجلات التدقيق'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name} - {self.timestamp}"


class Notification(models.Model):
    """
    Notifications for users
    الإشعارات للمستخدمين
    """
    NOTIFICATION_TYPES = [
        ('info', 'معلومات'),
        ('success', 'نجاح'),
        ('warning', 'تحذير'),
        ('error', 'خطأ'),
    ]
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='المستخدم'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='العنوان'
    )
    message = models.TextField(
        verbose_name='الرسالة'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name='نوع الإشعار'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='مقروء'
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='الرابط'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ القراءة'
    )
    
    class Meta:
        db_table = 'Tbl_Notifications'
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

