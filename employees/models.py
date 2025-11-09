"""
Employee models for comprehensive employee management
"""
from django.db import models
from core.models import BaseModel
from django.core.validators import FileExtensionValidator


class Employee(BaseModel):
    """
    Main Employee model
    نموذج الموظف الرئيسي
    """
    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'أعزب'),
        ('married', 'متزوج'),
        ('divorced', 'مطلق'),
        ('widowed', 'أرمل'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'دوام كامل'),
        ('part_time', 'دوام جزئي'),
        ('contract', 'عقد'),
        ('temporary', 'مؤقت'),
        ('intern', 'متدرب'),
    ]
    
    # Basic Information
    emp_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رمز الموظف'
    )
    first_name_ar = models.CharField(
        max_length=100,
        verbose_name='الاسم الأول بالعربية'
    )
    middle_name_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='الاسم الأوسط بالعربية'
    )
    last_name_ar = models.CharField(
        max_length=100,
        verbose_name='اسم العائلة بالعربية'
    )
    first_name_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='الاسم الأول بالإنجليزية'
    )
    last_name_en = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='اسم العائلة بالإنجليزية'
    )
    
    # Personal Information
    national_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الهوية الوطنية'
    )
    passport_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='رقم جواز السفر'
    )
    date_of_birth = models.DateField(
        verbose_name='تاريخ الميلاد'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='الجنس'
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        default='single',
        verbose_name='الحالة الاجتماعية'
    )
    nationality = models.CharField(
        max_length=100,
        default='سعودي',
        verbose_name='الجنسية'
    )
    religion = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الديانة'
    )
    
    # Contact Information
    email = models.EmailField(
        unique=True,
        verbose_name='البريد الإلكتروني'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='رقم الجوال'
    )
    address = models.TextField(
        verbose_name='العنوان'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='المدينة'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='الرمز البريدي'
    )
    
    # Employment Information
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees',
        verbose_name='القسم'
    )
    position = models.ForeignKey(
        'organization.Position',
        on_delete=models.SET_NULL,
        null=True,
        related_name='employees',
        verbose_name='المنصب'
    )
    branch = models.ForeignKey(
        'organization.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='الفرع'
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name='المدير المباشر'
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time',
        verbose_name='نوع التوظيف'
    )
    hire_date = models.DateField(
        verbose_name='تاريخ التعيين'
    )
    probation_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ انتهاء فترة التجربة'
    )
    confirmation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ التثبيت'
    )
    
    # Salary Information
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
    
    # Work Schedule
    work_shift = models.ForeignKey(
        'organization.WorkShift',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='الوردية'
    )
    
    # Leave Balances
    annual_leave_balance = models.IntegerField(
        default=21,
        verbose_name='رصيد الإجازة السنوية'
    )
    sick_leave_balance = models.IntegerField(
        default=30,
        verbose_name='رصيد الإجازة المرضية'
    )
    
    # Bank Information
    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='اسم البنك'
    )
    bank_account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='رقم الحساب البنكي'
    )
    iban = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='رقم الآيبان'
    )
    
    # Photo
    photo = models.ImageField(
        upload_to='employees/photos/',
        blank=True,
        null=True,
        verbose_name='الصورة الشخصية'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط'
    )
    termination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ إنهاء الخدمة'
    )
    termination_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='سبب إنهاء الخدمة'
    )
    
    # ZK Device Integration
    zk_user_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='معرف جهاز البصمة'
    )
    
    class Meta:
        db_table = 'Tbl_Employees_New'
        verbose_name = 'موظف'
        verbose_name_plural = 'الموظفون'
        ordering = ['emp_code']
    
    def __str__(self):
        return f"{self.emp_code} - {self.get_full_name_ar()}"
    
    def get_full_name_ar(self):
        """Get full Arabic name"""
        parts = [self.first_name_ar]
        if self.middle_name_ar:
            parts.append(self.middle_name_ar)
        parts.append(self.last_name_ar)
        return ' '.join(parts)
    
    def get_full_name_en(self):
        """Get full English name"""
        if self.first_name_en and self.last_name_en:
            return f"{self.first_name_en} {self.last_name_en}"
        return self.get_full_name_ar()
    
    def get_total_salary(self):
        """Calculate total salary"""
        return (self.basic_salary + self.housing_allowance + 
                self.transport_allowance + self.other_allowances)
    
    def get_age(self):
        """Calculate employee age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def get_years_of_service(self):
        """Calculate years of service"""
        from datetime import date
        today = date.today()
        return today.year - self.hire_date.year - (
            (today.month, today.day) < (self.hire_date.month, self.hire_date.day)
        )


class EmployeeDocument(BaseModel):
    """
    Employee documents (ID, passport, certificates, etc.)
    مستندات الموظف
    """
    DOCUMENT_TYPES = [
        ('national_id', 'الهوية الوطنية'),
        ('passport', 'جواز السفر'),
        ('certificate', 'شهادة'),
        ('contract', 'عقد'),
        ('medical', 'تقرير طبي'),
        ('other', 'أخرى'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='الموظف'
    )
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        verbose_name='نوع المستند'
    )
    document_name = models.CharField(
        max_length=200,
        verbose_name='اسم المستند'
    )
    document_file = models.FileField(
        upload_to='employees/documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        verbose_name='ملف المستند'
    )
    issue_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الإصدار'
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الانتهاء'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف'
    )

    class Meta:
        db_table = 'Tbl_Employee_Documents'
        verbose_name = 'مستند موظف'
        verbose_name_plural = 'مستندات الموظفين'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.document_name}"


class EmployeeContract(BaseModel):
    """
    Employee contracts
    عقود الموظفين
    """
    CONTRACT_TYPES = [
        ('permanent', 'دائم'),
        ('temporary', 'مؤقت'),
        ('probation', 'تجربة'),
        ('renewal', 'تجديد'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name='الموظف'
    )
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPES,
        verbose_name='نوع العقد'
    )
    contract_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='رقم العقد'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ النهاية'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='الراتب'
    )
    contract_file = models.FileField(
        upload_to='employees/contracts/',
        blank=True,
        null=True,
        verbose_name='ملف العقد'
    )
    terms_and_conditions = models.TextField(
        blank=True,
        null=True,
        verbose_name='الشروط والأحكام'
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name='العقد الحالي'
    )

    class Meta:
        db_table = 'Tbl_Employee_Contracts'
        verbose_name = 'عقد موظف'
        verbose_name_plural = 'عقود الموظفين'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.contract_number}"


class EmergencyContact(BaseModel):
    """
    Emergency contacts for employees
    جهات الاتصال في حالات الطوارئ
    """
    RELATIONSHIP_CHOICES = [
        ('spouse', 'زوج/زوجة'),
        ('parent', 'والد/والدة'),
        ('sibling', 'أخ/أخت'),
        ('child', 'ابن/ابنة'),
        ('friend', 'صديق'),
        ('other', 'أخرى'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='emergency_contacts',
        verbose_name='الموظف'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='الاسم'
    )
    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES,
        verbose_name='صلة القرابة'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='رقم الجوال'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='العنوان'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='جهة الاتصال الأساسية'
    )

    class Meta:
        db_table = 'Tbl_Emergency_Contacts'
        verbose_name = 'جهة اتصال طوارئ'
        verbose_name_plural = 'جهات اتصال الطوارئ'
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.name}"


class EmployeeEducation(BaseModel):
    """
    Employee education history
    المؤهلات التعليمية للموظف
    """
    DEGREE_CHOICES = [
        ('high_school', 'ثانوية عامة'),
        ('diploma', 'دبلوم'),
        ('bachelor', 'بكالوريوس'),
        ('master', 'ماجستير'),
        ('phd', 'دكتوراه'),
        ('other', 'أخرى'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='education',
        verbose_name='الموظف'
    )
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        verbose_name='الدرجة العلمية'
    )
    field_of_study = models.CharField(
        max_length=200,
        verbose_name='مجال الدراسة'
    )
    institution = models.CharField(
        max_length=200,
        verbose_name='المؤسسة التعليمية'
    )
    country = models.CharField(
        max_length=100,
        verbose_name='الدولة'
    )
    graduation_year = models.IntegerField(
        verbose_name='سنة التخرج'
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='التقدير'
    )
    certificate_file = models.FileField(
        upload_to='employees/certificates/',
        blank=True,
        null=True,
        verbose_name='ملف الشهادة'
    )

    class Meta:
        db_table = 'Tbl_Employee_Education'
        verbose_name = 'مؤهل تعليمي'
        verbose_name_plural = 'المؤهلات التعليمية'
        ordering = ['-graduation_year']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.get_degree_display()}"


class EmployeeExperience(BaseModel):
    """
    Employee work experience
    الخبرات العملية للموظف
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='experience',
        verbose_name='الموظف'
    )
    company_name = models.CharField(
        max_length=200,
        verbose_name='اسم الشركة'
    )
    position = models.CharField(
        max_length=200,
        verbose_name='المنصب'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ النهاية'
    )
    is_current = models.BooleanField(
        default=False,
        verbose_name='الوظيفة الحالية'
    )
    responsibilities = models.TextField(
        blank=True,
        null=True,
        verbose_name='المسؤوليات'
    )
    reason_for_leaving = models.TextField(
        blank=True,
        null=True,
        verbose_name='سبب ترك العمل'
    )

    class Meta:
        db_table = 'Tbl_Employee_Experience'
        verbose_name = 'خبرة عملية'
        verbose_name_plural = 'الخبرات العملية'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.company_name}"

