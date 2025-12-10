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
        max_length=50,
        verbose_name='الاسم الأول بالعربية'
    )
    second_name_ar = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الاسم الثاني بالعربية'
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
    full_name_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='الاسم الكامل بالعربية'
    )
    first_name_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الاسم الأول بالإنجليزية'
    )
    last_name_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='اسم العائلة بالإنجليزية'
    )
    full_name_en = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الاسم الكامل بالإنجليزية'
    )
    mother_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='اسم الأم'
    )

    # Personal Information
    national_id = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='رقم الهوية الوطنية'
    )
    national_id_expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ انتهاء الهوية'
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
    place_of_birth = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='مكان الميلاد'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='الجنس'
    )
    marital_status = models.CharField(
        max_length=50,
        choices=MARITAL_STATUS_CHOICES,
        default='single',
        verbose_name='الحالة الاجتماعية'
    )
    nationality = models.CharField(
        max_length=50,
        default='سعودي',
        verbose_name='الجنسية'
    )
    religion = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الديانة'
    )
    people_with_special_needs = models.BooleanField(
        default=False,
        verbose_name='من ذوي الاحتياجات الخاصة'
    )
    governorate = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='المحافظة'
    )

    # Contact Information
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='البريد الإلكتروني'
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='رقم الهاتف 1'
    )
    phone2 = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='رقم الهاتف 2'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='رقم الجوال'
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='العنوان'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='المدينة'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='الرمز البريدي'
    )
    telegram_id = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name='معرف تيليجرام'
    )

    # Employment Information
    department = models.ForeignKey(
        'organization.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='القسم'
    )
    position = models.ForeignKey(
        'organization.Position',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time',
        blank=True,
        null=True,
        verbose_name='نوع الموظف'
    )
    working_condition = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='حالة العمل'
    )
    hire_date = models.DateField(
        null=True,
        blank=True,
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
    total_salary = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='إجمالي الراتب'
    )
    total_salary_text = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='إجمالي الراتب نصاً'
    )
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
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

    # Work Schedule & Shift Information
    work_shift = models.ForeignKey(
        'organization.WorkShift',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='الوردية'
    )
    current_week_shift = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='وردية الأسبوع الحالي'
    )
    next_week_shift = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='وردية الأسبوع القادم'
    )
    friday_operation = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='عمل يوم الجمعة'
    )
    shift_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='نوع الوردية'
    )
    shift_paper = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='ورقة الوردية'
    )

    # Transportation Information
    has_car = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='لديه سيارة'
    )
    car_ride_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='وقت ركوب السيارة'
    )
    car_pickup_point = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='نقطة التقاط السيارة'
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

    # Social Insurance Information
    insurance_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='حالة التأمين'
    )
    insurance_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='رقم التأمين'
    )
    insurance_code = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='كود التأمين'
    )
    insurance_job_code = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='كود الوظيفة للتأمين'
    )
    insurance_job_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='اسم الوظيفة للتأمين'
    )
    insurance_start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ بداية التأمين'
    )
    insurance_salary = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='راتب التأمين'
    )
    insurance_percentage = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='نسبة التأمين المستحقة'
    )
    insurance_amount_due = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='مبلغ التأمين المستحق'
    )

    # Insurance Forms
    form_s1 = models.BooleanField(
        default=False,
        verbose_name='نموذج 1'
    )
    form_s1_delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ تسليم نموذج 1'
    )
    form_s1_receive_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ استلام نموذج 1'
    )
    form_s1_entry_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='رقم دخول نموذج 1'
    )
    form_s1_entry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ دخول نموذج 1'
    )
    insurance_entry_confirmation = models.BooleanField(
        default=False,
        verbose_name='تأكيد دخول التأمين'
    )

    form_s6 = models.BooleanField(
        default=False,
        verbose_name='نموذج 6'
    )
    form_s6_delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ تسليم نموذج 6'
    )
    form_s6_receive_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ استلام نموذج 6'
    )
    form_s6_entry_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='رقم دخول نموذج 6'
    )
    form_s6_entry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ دخول نموذج 6'
    )
    confirm_exit_insurance = models.BooleanField(
        default=False,
        verbose_name='تأكيد خروج التأمين'
    )

    # Health Insurance Information
    health_card = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='البطاقة الصحية'
    )
    health_card_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='رقم البطاقة الصحية'
    )
    health_card_start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ بداية البطاقة الصحية'
    )
    health_card_renewal_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ تجديد البطاقة الصحية'
    )
    health_card_remaining_days = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='الأيام المتبقية لانتهاء البطاقة الصحية'
    )

    # International Insurance (Orient/ElDawliya)
    orient_subscription_start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ بداية اشتراك الدولية'
    )
    orient_subscription_expiry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ انتهاء اشتراك الدولية'
    )
    orient_incoming_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='رقم وارد الدولية'
    )
    orient_incoming_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ وارد الدولية'
    )
    orient_s1 = models.BooleanField(
        default=False,
        verbose_name='نموذج 1 الدولية'
    )
    orient_s1_delivery_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ تسليم نموذج 1 الدولية'
    )
    orient_s1_receipt_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ استلام نموذج 1 الدولية'
    )
    orient_insurance_entry_confirmation = models.BooleanField(
        default=False,
        verbose_name='تأكيد دخول تأمين الدولية'
    )
    orient_s6 = models.BooleanField(
        default=False,
        verbose_name='نموذج 6 الدولية'
    )

    # Contract Information
    contract_renewal_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='تاريخ تجديد العقد'
    )
    contract_renewal_month = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='شهر تجديد العقد'
    )
    remaining_contract_renewal = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='المتبقي لتجديد العقد'
    )
    years_since_contract_start = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='السنوات منذ بداية العقد'
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

    # Document Submission Flags
    military_service_certificate = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='شهادة الخدمة العسكرية'
    )
    qualification_certificate = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='شهادة المؤهل'
    )
    birth_certificate = models.BooleanField(
        default=False,
        verbose_name='شهادة الميلاد'
    )
    insurance_printout = models.BooleanField(
        default=False,
        verbose_name='مطبوعة التأمينات'
    )
    id_card_photo = models.BooleanField(
        default=False,
        verbose_name='صورة البطاقة'
    )
    personal_photos = models.BooleanField(
        default=False,
        verbose_name='صور شخصية'
    )
    employment_contract_submitted = models.BooleanField(
        default=False,
        verbose_name='عقد العمل'
    )
    medical_exam_form_submitted = models.BooleanField(
        default=False,
        verbose_name='نموذج الفحص الطبي'
    )
    medical_exam_form_submission = models.BooleanField(
        default=False,
        verbose_name='تقديم نموذج الفحص الطبي'
    )
    criminal_record_check = models.BooleanField(
        default=False,
        verbose_name='فيش وتشبيه'
    )
    social_status_report = models.BooleanField(
        default=False,
        verbose_name='بحث حالة اجتماعية'
    )
    skill_level_measurement_certificate = models.BooleanField(
        default=False,
        verbose_name='شهادة قياس مستوى المهارة'
    )

    # Work Heel (كعب العمل)
    work_heel = models.BooleanField(
        default=False,
        verbose_name='كعب العمل'
    )
    work_heel_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='رقم كعب العمل'
    )
    work_heel_recipient = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='مستلم كعب العمل'
    )
    work_heel_recipient_address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='عنوان مستلم كعب العمل'
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
    resignation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الاستقالة'
    )
    termination_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='سبب إنهاء الخدمة'
    )
    resignation_reason = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='سبب الاستقالة'
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
        if self.full_name_ar:
            return self.full_name_ar
        parts = [self.first_name_ar]
        if self.second_name_ar:
            parts.append(self.second_name_ar)
        if self.middle_name_ar:
            parts.append(self.middle_name_ar)
        parts.append(self.last_name_ar)
        return ' '.join(parts)

    def get_full_name_en(self):
        """Get full English name"""
        if self.full_name_en:
            return self.full_name_en
        if self.first_name_en and self.last_name_en:
            return f"{self.first_name_en} {self.last_name_en}"
        return self.get_full_name_ar()

    def get_total_salary(self):
        """Calculate total salary"""
        if self.total_salary:
            return self.total_salary
        if self.basic_salary:
            return (self.basic_salary + self.housing_allowance +
                    self.transport_allowance + self.other_allowances)
        return 0

    def get_calculated_basic_salary(self):
        """Calculate basic salary from total (Total / 1.30)"""
        if self.total_salary:
            return round(self.total_salary / 1.30, 2)
        return self.basic_salary or 0

    def get_calculated_allowances(self):
        """Calculate allowances from total (Total - Basic)"""
        if self.total_salary:
            basic = self.get_calculated_basic_salary()
            return round(self.total_salary - basic, 2)
        return (self.housing_allowance + self.transport_allowance + self.other_allowances)

    def get_age(self):
        """Calculate employee age"""
        from datetime import date
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age

    def get_years_of_service(self):
        """Calculate years of service"""
        from datetime import date
        if not self.hire_date:
            return None
        today = date.today()
        years = today.year - self.hire_date.year - (
            (today.month, today.day) < (self.hire_date.month, self.hire_date.day)
        )
        return years

    def get_probation_end_date(self):
        """Calculate probation end date (3 months from hire date)"""
        if self.probation_end_date:
            return self.probation_end_date
        if self.hire_date:
            from dateutil.relativedelta import relativedelta
            return self.hire_date + relativedelta(months=3)
        return None

    def get_health_card_expiry_date(self):
        """Calculate health card expiry date (1 year from renewal date)"""
        if self.health_card_renewal_date:
            from dateutil.relativedelta import relativedelta
            return self.health_card_renewal_date + relativedelta(years=1)
        return None

    def get_contract_expiry_date(self):
        """Calculate contract expiry date (1 year from renewal date)"""
        if self.contract_renewal_date:
            from dateutil.relativedelta import relativedelta
            return self.contract_renewal_date + relativedelta(years=1)
        return None

    def get_hiring_date_health_card(self):
        """Calculate hiring date for health card (3 months before insurance start)"""
        if self.insurance_start_date:
            from dateutil.relativedelta import relativedelta
            return self.insurance_start_date - relativedelta(months=3)
        return None

    def get_work_heel_registration_date(self):
        """Calculate work heel registration date (1 month after hire date)"""
        if self.hire_date:
            from dateutil.relativedelta import relativedelta
            return self.hire_date + relativedelta(months=1)
        return None


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



class EmployeeInsurance(BaseModel):
    """
    Employee insurance information (Social & Health)
    بيانات التأمينات الاجتماعية والصحية للموظف
    """
    INSURANCE_TYPE_CHOICES = [
        ('social', 'تأمينات اجتماعية'),
        ('health', 'تأمين صحي'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='insurances',
        verbose_name='الموظف'
    )
    insurance_type = models.CharField(
        max_length=20,
        choices=INSURANCE_TYPE_CHOICES,
        verbose_name='نوع التأمين'
    )
    insurance_number = models.CharField(
        max_length=50,
        verbose_name='رقم التأمين'
    )
    insurance_company = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='شركة التأمين'
    )
    start_date = models.DateField(
        verbose_name='تاريخ البداية'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ النهاية'
    )
    coverage_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='قيمة التغطية'
    )
    monthly_premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='القسط الشهري'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )

    class Meta:
        db_table = 'Tbl_Employee_Insurance'
        verbose_name = 'تأمين موظف'
        verbose_name_plural = 'تأمينات الموظفين'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.get_insurance_type_display()}"


class EmployeeCustody(BaseModel):
    """
    Employee custody items (equipment, tools, etc.)
    عهد الموظف
    """
    CUSTODY_TYPE_CHOICES = [
        ('laptop', 'جهاز كمبيوتر محمول'),
        ('desktop', 'جهاز كمبيوتر مكتبي'),
        ('mobile', 'هاتف محمول'),
        ('vehicle', 'مركبة'),
        ('tools', 'أدوات'),
        ('keys', 'مفاتيح'),
        ('card', 'بطاقة'),
        ('other', 'أخرى'),
    ]

    CUSTODY_STATUS_CHOICES = [
        ('active', 'نشطة'),
        ('returned', 'مُرتجعة'),
        ('lost', 'مفقودة'),
        ('damaged', 'تالفة'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='custodies',
        verbose_name='الموظف'
    )
    custody_type = models.CharField(
        max_length=20,
        choices=CUSTODY_TYPE_CHOICES,
        verbose_name='نوع العهدة'
    )
    item_name = models.CharField(
        max_length=200,
        verbose_name='اسم الصنف'
    )
    item_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='وصف الصنف'
    )
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='الرقم التسلسلي'
    )
    item_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='قيمة الصنف'
    )
    issue_date = models.DateField(
        verbose_name='تاريخ الاستلام'
    )
    return_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='تاريخ الإرجاع'
    )
    status = models.CharField(
        max_length=20,
        choices=CUSTODY_STATUS_CHOICES,
        default='active',
        verbose_name='الحالة'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )

    class Meta:
        db_table = 'Tbl_Employee_Custody'
        verbose_name = 'عهدة موظف'
        verbose_name_plural = 'عهد الموظفين'
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.item_name}"


class EmployeeQualification(BaseModel):
    """
    Employee educational qualifications
    المؤهلات الدراسية للموظف
    """
    EDUCATION_LEVEL_CHOICES = [
        ('primary', 'ابتدائي'),
        ('intermediate', 'متوسط'),
        ('secondary', 'ثانوي'),
        ('diploma', 'دبلوم'),
        ('bachelor', 'بكالوريوس'),
        ('master', 'ماجستير'),
        ('doctorate', 'دكتوراه'),
        ('other', 'أخرى'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='qualifications',
        verbose_name='الموظف'
    )
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name='المستوى التعليمي'
    )
    major = models.CharField(
        max_length=200,
        verbose_name='التخصص'
    )
    institution_name = models.CharField(
        max_length=200,
        verbose_name='اسم المؤسسة التعليمية'
    )
    graduation_year = models.IntegerField(
        verbose_name='سنة التخرج'
    )
    grade = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='الدرجة/التقدير'
    )
    certificate_file = models.FileField(
        upload_to='employees/certificates/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name='ملف الشهادة'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )

    class Meta:
        db_table = 'Tbl_Employee_Qualifications'
        verbose_name = 'مؤهل موظف'
        verbose_name_plural = 'مؤهلات الموظفين'
        ordering = ['-graduation_year']

    def __str__(self):
        return f"{self.employee.emp_code} - {self.get_education_level_display()}"
