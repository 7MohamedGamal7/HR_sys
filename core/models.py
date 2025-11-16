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
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='أنشئ بواسطة'
    )
    updated_by = models.ForeignKey(
        'core.User',
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


class CompanySettings(models.Model):
    """
    Comprehensive company and system settings (Singleton pattern)
    إعدادات الشركة والنظام الشاملة
    """
    # Company Information
    company_name_ar = models.CharField(
        max_length=200,
        default='نظام إدارة الموارد البشرية',
        verbose_name='اسم الشركة (عربي)'
    )
    company_name_en = models.CharField(
        max_length=200,
        default='HR Management System',
        verbose_name='اسم الشركة (إنجليزي)'
    )
    company_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='عنوان الشركة'
    )
    company_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='هاتف الشركة'
    )
    company_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='البريد الإلكتروني'
    )
    company_website = models.URLField(
        blank=True,
        null=True,
        verbose_name='الموقع الإلكتروني'
    )
    company_logo = models.ImageField(
        upload_to='company/',
        blank=True,
        null=True,
        verbose_name='شعار الشركة'
    )

    # UI/UX Settings
    FONT_CHOICES = [
        ('Cairo', 'Cairo'),
        ('Tajawal', 'Tajawal'),
        ('Almarai', 'Almarai'),
        ('Amiri', 'Amiri'),
        ('Noto Sans Arabic', 'Noto Sans Arabic'),
    ]
    font_family = models.CharField(
        max_length=50,
        choices=FONT_CHOICES,
        default='Cairo',
        verbose_name='نوع الخط'
    )

    FONT_SIZE_CHOICES = [
        ('small', 'صغير'),
        ('medium', 'متوسط'),
        ('large', 'كبير'),
    ]
    font_size = models.CharField(
        max_length=10,
        choices=FONT_SIZE_CHOICES,
        default='medium',
        verbose_name='حجم الخط'
    )

    theme_color = models.CharField(
        max_length=7,
        default='#667eea',
        verbose_name='اللون الأساسي'
    )

    rtl_enabled = models.BooleanField(
        default=True,
        verbose_name='تفعيل الاتجاه من اليمين لليسار'
    )

    DATE_FORMAT_CHOICES = [
        ('d/m/Y', 'يوم/شهر/سنة'),
        ('Y-m-d', 'سنة-شهر-يوم'),
        ('d-m-Y', 'يوم-شهر-سنة'),
    ]
    date_format = models.CharField(
        max_length=10,
        choices=DATE_FORMAT_CHOICES,
        default='d/m/Y',
        verbose_name='تنسيق التاريخ'
    )

    TIME_FORMAT_CHOICES = [
        ('12', '12 ساعة'),
        ('24', '24 ساعة'),
    ]
    time_format = models.CharField(
        max_length=2,
        choices=TIME_FORMAT_CHOICES,
        default='12',
        verbose_name='تنسيق الوقت'
    )

    # System Settings
    LANGUAGE_CHOICES = [
        ('ar', 'العربية'),
        ('en', 'English'),
    ]
    default_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ar',
        verbose_name='اللغة الافتراضية'
    )

    timezone = models.CharField(
        max_length=50,
        default='Asia/Riyadh',
        verbose_name='المنطقة الزمنية'
    )

    CURRENCY_CHOICES = [
        ('SAR', 'ريال سعودي'),
        ('USD', 'دولار أمريكي'),
        ('EUR', 'يورو'),
        ('AED', 'درهم إماراتي'),
    ]
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='SAR',
        verbose_name='العملة'
    )

    pagination_size = models.IntegerField(
        default=20,
        verbose_name='عدد السجلات في الصفحة'
    )

    session_timeout = models.IntegerField(
        default=30,
        verbose_name='مدة انتهاء الجلسة (دقيقة)'
    )

    # Email Configuration
    smtp_server = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='خادم SMTP'
    )
    smtp_port = models.IntegerField(
        default=587,
        verbose_name='منفذ SMTP'
    )
    smtp_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='اسم مستخدم SMTP'
    )
    smtp_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='كلمة مرور SMTP'
    )
    email_notifications_enabled = models.BooleanField(
        default=True,
        verbose_name='تفعيل إشعارات البريد الإلكتروني'
    )

    # Security Settings
    password_min_length = models.IntegerField(
        default=8,
        verbose_name='الحد الأدنى لطول كلمة المرور'
    )
    password_require_uppercase = models.BooleanField(
        default=True,
        verbose_name='يتطلب أحرف كبيرة'
    )
    password_require_lowercase = models.BooleanField(
        default=True,
        verbose_name='يتطلب أحرف صغيرة'
    )
    password_require_numbers = models.BooleanField(
        default=True,
        verbose_name='يتطلب أرقام'
    )
    password_require_special = models.BooleanField(
        default=False,
        verbose_name='يتطلب رموز خاصة'
    )
    two_factor_enabled = models.BooleanField(
        default=False,
        verbose_name='تفعيل المصادقة الثنائية'
    )
    max_login_attempts = models.IntegerField(
        default=5,
        verbose_name='الحد الأقصى لمحاولات تسجيل الدخول'
    )

    # Metadata
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='تم التحديث بواسطة'
    )

    class Meta:
        db_table = 'Tbl_Company_Settings'
        verbose_name = 'إعدادات الشركة'
        verbose_name_plural = 'إعدادات الشركة'

    def __str__(self):
        return f"إعدادات {self.company_name_ar}"

    def save(self, *args, **kwargs):
        # Singleton pattern - only one instance allowed
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Load the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


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

