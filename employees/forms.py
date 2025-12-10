"""
Forms for employees app
نماذج تطبيق الموظفين
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab
from .models import (
    Employee, EmployeeDocument, EmployeeContract,
    EmergencyContact, EmployeeEducation, EmployeeExperience,
    EmployeeInsurance, EmployeeCustody
)


class EmployeeForm(forms.ModelForm):
    """
    Employee creation/edit form
    نموذج إضافة/تعديل موظف
    """
    class Meta:
        model = Employee
        fields = [
            # Basic Information
            'emp_code', 'first_name_ar', 'second_name_ar', 'middle_name_ar', 'last_name_ar',
            'full_name_ar', 'first_name_en', 'last_name_en', 'full_name_en', 'mother_name',
            # Personal Information
            'national_id', 'national_id_expiry_date', 'passport_number',
            'date_of_birth', 'place_of_birth', 'gender', 'marital_status', 'nationality',
            'religion', 'people_with_special_needs', 'governorate',
            # Contact Information
            'email', 'phone', 'phone2', 'mobile', 'address', 'city', 'postal_code', 'telegram_id',
            # Employment Information
            'department', 'position', 'branch', 'manager', 'hire_date', 'employment_type',
            'working_condition', 'probation_end_date', 'confirmation_date',
            # Work Schedule
            'work_shift', 'current_week_shift', 'next_week_shift', 'friday_operation',
            'shift_type', 'shift_paper',
            # Transportation
            'has_car', 'car_ride_time', 'car_pickup_point',
            # Salary Information
            'total_salary', 'total_salary_text', 'basic_salary',
            'housing_allowance', 'transport_allowance', 'other_allowances',
            # Leave Balances
            'annual_leave_balance', 'sick_leave_balance',
            # Social Insurance
            'insurance_status', 'insurance_number', 'insurance_code',
            'insurance_job_code', 'insurance_job_name', 'insurance_start_date',
            'insurance_salary', 'insurance_percentage', 'insurance_amount_due',
            # Insurance Forms
            'form_s1', 'form_s1_delivery_date', 'form_s1_receive_date',
            'form_s1_entry_number', 'form_s1_entry_date', 'insurance_entry_confirmation',
            'form_s6', 'form_s6_delivery_date', 'form_s6_receive_date',
            'form_s6_entry_number', 'form_s6_entry_date', 'confirm_exit_insurance',
            # Health Insurance
            'health_card', 'health_card_number', 'health_card_start_date',
            'health_card_renewal_date', 'health_card_remaining_days',
            # International Insurance
            'orient_subscription_start_date', 'orient_subscription_expiry_date',
            'orient_incoming_number', 'orient_incoming_date',
            'orient_s1', 'orient_s1_delivery_date', 'orient_s1_receipt_date',
            'orient_insurance_entry_confirmation', 'orient_s6',
            # Contract Information
            'contract_renewal_date', 'contract_renewal_month',
            'remaining_contract_renewal', 'years_since_contract_start',
            # Bank Information
            'bank_name', 'bank_account_number', 'iban',
            # Document Submission
            'military_service_certificate', 'qualification_certificate',
            'birth_certificate', 'insurance_printout', 'id_card_photo',
            'personal_photos', 'employment_contract_submitted', 'medical_exam_form_submitted',
            'medical_exam_form_submission', 'criminal_record_check',
            'social_status_report', 'skill_level_measurement_certificate',
            # Work Heel
            'work_heel', 'work_heel_number', 'work_heel_recipient', 'work_heel_recipient_address',
            # Other
            'photo', 'zk_user_id',
            # Status
            'is_active', 'termination_date', 'resignation_date',
            'termination_reason', 'resignation_reason'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'national_id_expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'probation_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'termination_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resignation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'insurance_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s1_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s1_receive_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s1_entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s6_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s6_receive_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'form_s6_entry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'health_card_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'health_card_renewal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orient_subscription_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orient_subscription_expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orient_incoming_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orient_s1_delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'orient_s1_receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contract_renewal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'car_ride_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'termination_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False

        # Filter querysets to show only active records
        from organization.models import Department, Position, Branch, WorkShift
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        self.fields['position'].queryset = Position.objects.filter(is_active=True)
        self.fields['branch'].queryset = Branch.objects.filter(is_active=True)
        self.fields['work_shift'].queryset = WorkShift.objects.filter(is_active=True)
        self.fields['manager'].queryset = Employee.objects.filter(is_active=True)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'البيانات الشخصية',
                    HTML('<h5 class="mb-3">المعلومات الأساسية</h5>'),
                    Row(
                        Column('emp_code', css_class='col-md-3'),
                        Column('photo', css_class='col-md-9'),
                    ),
                    Row(
                        Column('first_name_ar', css_class='col-md-3'),
                        Column('second_name_ar', css_class='col-md-3'),
                        Column('middle_name_ar', css_class='col-md-3'),
                        Column('last_name_ar', css_class='col-md-3'),
                    ),
                    Row(
                        Column('full_name_ar', css_class='col-md-6'),
                        Column('mother_name', css_class='col-md-6'),
                    ),
                    Row(
                        Column('first_name_en', css_class='col-md-4'),
                        Column('last_name_en', css_class='col-md-4'),
                        Column('full_name_en', css_class='col-md-4'),
                    ),
                    HTML('<hr><h5 class="mb-3">البيانات الشخصية</h5>'),
                    Row(
                        Column('national_id', css_class='col-md-4'),
                        Column('national_id_expiry_date', css_class='col-md-4'),
                        Column('passport_number', css_class='col-md-4'),
                    ),
                    Row(
                        Column('date_of_birth', css_class='col-md-4'),
                        Column('place_of_birth', css_class='col-md-4'),
                        Column('gender', css_class='col-md-4'),
                    ),
                    Row(
                        Column('marital_status', css_class='col-md-4'),
                        Column('nationality', css_class='col-md-4'),
                        Column('religion', css_class='col-md-4'),
                    ),
                    Row(
                        Column('governorate', css_class='col-md-6'),
                        Column('people_with_special_needs', css_class='col-md-6'),
                    ),
                    HTML('<hr><h5 class="mb-3">معلومات الاتصال</h5>'),
                    Row(
                        Column('email', css_class='col-md-6'),
                        Column('telegram_id', css_class='col-md-6'),
                    ),
                    Row(
                        Column('phone', css_class='col-md-4'),
                        Column('phone2', css_class='col-md-4'),
                        Column('mobile', css_class='col-md-4'),
                    ),
                    Row(
                        Column('address', css_class='col-md-8'),
                        Column('city', css_class='col-md-4'),
                    ),
                    'postal_code',
                ),
                Tab(
                    'بيانات العمل',
                    HTML('<h5 class="mb-3">معلومات الوظيفة</h5>'),
                    Row(
                        Column('department', css_class='col-md-6'),
                        Column('position', css_class='col-md-6'),
                    ),
                    Row(
                        Column('branch', css_class='col-md-6'),
                        Column('manager', css_class='col-md-6'),
                    ),
                    Row(
                        Column('hire_date', css_class='col-md-4'),
                        Column('employment_type', css_class='col-md-4'),
                        Column('working_condition', css_class='col-md-4'),
                    ),
                    Row(
                        Column('probation_end_date', css_class='col-md-6'),
                        Column('confirmation_date', css_class='col-md-6'),
                    ),
                    HTML('<hr><h5 class="mb-3">معلومات الوردية</h5>'),
                    Row(
                        Column('work_shift', css_class='col-md-4'),
                        Column('shift_type', css_class='col-md-4'),
                        Column('shift_paper', css_class='col-md-4'),
                    ),
                    Row(
                        Column('current_week_shift', css_class='col-md-4'),
                        Column('next_week_shift', css_class='col-md-4'),
                        Column('friday_operation', css_class='col-md-4'),
                    ),
                    HTML('<hr><h5 class="mb-3">معلومات النقل</h5>'),
                    Row(
                        Column('has_car', css_class='col-md-4'),
                        Column('car_ride_time', css_class='col-md-4'),
                        Column('car_pickup_point', css_class='col-md-4'),
                    ),
                    Row(
                        Column('zk_user_id', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'بيانات الراتب',
                    HTML('<h5 class="mb-3">معلومات الراتب</h5>'),
                    Row(
                        Column('total_salary', css_class='col-md-6'),
                        Column('total_salary_text', css_class='col-md-6'),
                    ),
                    Row(
                        Column('basic_salary', css_class='col-md-6'),
                        Column('housing_allowance', css_class='col-md-6'),
                    ),
                    Row(
                        Column('transport_allowance', css_class='col-md-6'),
                        Column('other_allowances', css_class='col-md-6'),
                    ),
                    HTML('<hr><h5 class="mb-3">أرصدة الإجازات</h5>'),
                    Row(
                        Column('annual_leave_balance', css_class='col-md-6'),
                        Column('sick_leave_balance', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'التأمينات الاجتماعية',
                    HTML('<h5 class="mb-3">معلومات التأمين</h5>'),
                    Row(
                        Column('insurance_status', css_class='col-md-4'),
                        Column('insurance_number', css_class='col-md-4'),
                        Column('insurance_code', css_class='col-md-4'),
                    ),
                    Row(
                        Column('insurance_job_code', css_class='col-md-6'),
                        Column('insurance_job_name', css_class='col-md-6'),
                    ),
                    Row(
                        Column('insurance_start_date', css_class='col-md-4'),
                        Column('insurance_salary', css_class='col-md-4'),
                        Column('insurance_percentage', css_class='col-md-4'),
                    ),
                    'insurance_amount_due',
                    HTML('<hr><h5 class="mb-3">نموذج 1</h5>'),
                    Row(
                        Column('form_s1', css_class='col-md-3'),
                        Column('form_s1_delivery_date', css_class='col-md-3'),
                        Column('form_s1_receive_date', css_class='col-md-3'),
                        Column('insurance_entry_confirmation', css_class='col-md-3'),
                    ),
                    Row(
                        Column('form_s1_entry_number', css_class='col-md-6'),
                        Column('form_s1_entry_date', css_class='col-md-6'),
                    ),
                    HTML('<hr><h5 class="mb-3">نموذج 6</h5>'),
                    Row(
                        Column('form_s6', css_class='col-md-3'),
                        Column('form_s6_delivery_date', css_class='col-md-3'),
                        Column('form_s6_receive_date', css_class='col-md-3'),
                        Column('confirm_exit_insurance', css_class='col-md-3'),
                    ),
                    Row(
                        Column('form_s6_entry_number', css_class='col-md-6'),
                        Column('form_s6_entry_date', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'التأمين الصحي',
                    HTML('<h5 class="mb-3">البطاقة الصحية</h5>'),
                    Row(
                        Column('health_card', css_class='col-md-6'),
                        Column('health_card_number', css_class='col-md-6'),
                    ),
                    Row(
                        Column('health_card_start_date', css_class='col-md-4'),
                        Column('health_card_renewal_date', css_class='col-md-4'),
                        Column('health_card_remaining_days', css_class='col-md-4'),
                    ),
                    HTML('<hr><h5 class="mb-3">تأمين الدولية (Orient)</h5>'),
                    Row(
                        Column('orient_subscription_start_date', css_class='col-md-6'),
                        Column('orient_subscription_expiry_date', css_class='col-md-6'),
                    ),
                    Row(
                        Column('orient_incoming_number', css_class='col-md-6'),
                        Column('orient_incoming_date', css_class='col-md-6'),
                    ),
                    Row(
                        Column('orient_s1', css_class='col-md-4'),
                        Column('orient_s1_delivery_date', css_class='col-md-4'),
                        Column('orient_s1_receipt_date', css_class='col-md-4'),
                    ),
                    Row(
                        Column('orient_insurance_entry_confirmation', css_class='col-md-6'),
                        Column('orient_s6', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'بيانات العقد',
                    HTML('<h5 class="mb-3">معلومات العقد</h5>'),
                    Row(
                        Column('contract_renewal_date', css_class='col-md-4'),
                        Column('contract_renewal_month', css_class='col-md-4'),
                        Column('remaining_contract_renewal', css_class='col-md-4'),
                    ),
                    'years_since_contract_start',
                ),
                Tab(
                    'البيانات البنكية',
                    HTML('<h5 class="mb-3">معلومات الحساب البنكي</h5>'),
                    'bank_name',
                    Row(
                        Column('bank_account_number', css_class='col-md-6'),
                        Column('iban', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'مستندات التعيين',
                    HTML('<h5 class="mb-3">الشهادات والمستندات</h5>'),
                    Row(
                        Column('military_service_certificate', css_class='col-md-6'),
                        Column('qualification_certificate', css_class='col-md-6'),
                    ),
                    Row(
                        Column('birth_certificate', css_class='col-md-3'),
                        Column('insurance_printout', css_class='col-md-3'),
                        Column('id_card_photo', css_class='col-md-3'),
                        Column('personal_photos', css_class='col-md-3'),
                    ),
                    Row(
                        Column('employment_contract_submitted', css_class='col-md-3'),
                        Column('medical_exam_form_submitted', css_class='col-md-3'),
                        Column('medical_exam_form_submission', css_class='col-md-3'),
                        Column('criminal_record_check', css_class='col-md-3'),
                    ),
                    Row(
                        Column('social_status_report', css_class='col-md-6'),
                        Column('skill_level_measurement_certificate', css_class='col-md-6'),
                    ),
                    HTML('<hr><h5 class="mb-3">كعب العمل</h5>'),
                    Row(
                        Column('work_heel', css_class='col-md-3'),
                        Column('work_heel_number', css_class='col-md-3'),
                        Column('work_heel_recipient', css_class='col-md-3'),
                        Column('work_heel_recipient_address', css_class='col-md-3'),
                    ),
                ),
                Tab(
                    'حالة الموظف',
                    HTML('<h5 class="mb-3">حالة التوظيف</h5>'),
                    'is_active',
                    Row(
                        Column('termination_date', css_class='col-md-6'),
                        Column('resignation_date', css_class='col-md-6'),
                    ),
                    Row(
                        Column('termination_reason', css_class='col-md-6'),
                        Column('resignation_reason', css_class='col-md-6'),
                    ),
                ),
            ),
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML("<a href=\"{% url 'employees:employee_list' %}\" class=\"btn btn-secondary\">إلغاء</a>")
            )
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email or None


class EmployeeDocumentForm(forms.ModelForm):
    """
    Employee document form
    نموذج مستندات الموظف
    """
    class Meta:
        model = EmployeeDocument
        fields = ['document_type', 'document_name', 'document_file', 'issue_date', 'expiry_date', 'description']
        labels = {
            'document_type': 'نوع المستند',
            'document_name': 'اسم المستند',
            'document_file': 'ملف المستند',
            'issue_date': 'تاريخ الإصدار',
            'expiry_date': 'تاريخ الانتهاء',
            'description': 'الوصف',
        }
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'document_type',
            'document_name',
            Row(
                Column('issue_date', css_class='col-md-6'),
                Column('expiry_date', css_class='col-md-6'),
            ),
            'document_file',
            'description',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="javascript:history.back()" class="btn btn-secondary">إلغاء</a>')
            )
        )


class EmployeeContractForm(forms.ModelForm):
    """
    Employee contract form
    نموذج عقد الموظف
    """
    class Meta:
        model = EmployeeContract
        fields = [
            'contract_type', 'contract_number', 'start_date', 'end_date', 'salary',
            'contract_file', 'terms_and_conditions', 'is_current'
        ]
        labels = {
            'contract_type': 'نوع العقد',
            'contract_number': 'رقم العقد',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'salary': 'الراتب',
            'contract_file': 'ملف العقد',
            'terms_and_conditions': 'الشروط والأحكام',
            'is_current': 'العقد الحالي',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'terms_and_conditions': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'contract_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'contract_type',
            'contract_number',
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            'salary',
            'contract_file',
            'terms_and_conditions',
            'is_current',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="javascript:history.back()" class="btn btn-secondary">إلغاء</a>')
            )
        )


class EmergencyContactForm(forms.ModelForm):
    """
    Emergency contact form
    نموذج جهة الاتصال في حالات الطوارئ
    """
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone', 'mobile', 'address']
        labels = {
            'name': 'الاسم',
            'relationship': 'صلة القرابة',
            'phone': 'الهاتف',
            'mobile': 'الجوال',
            'address': 'العنوان',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'relationship',
            Row(
                Column('phone', css_class='col-md-6'),
                Column('mobile', css_class='col-md-6'),
            ),
            'address',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="javascript:history.back()" class="btn btn-secondary">إلغاء</a>')
            )
        )


class EmployeeEducationForm(forms.ModelForm):
    """
    Employee education form
    نموذج المؤهلات التعليمية
    """
    class Meta:
        model = EmployeeEducation
        fields = ['degree', 'field_of_study', 'institution', 'country', 'graduation_year', 'grade', 'certificate_file']
        labels = {
            'degree': 'الدرجة العلمية',
            'field_of_study': 'مجال الدراسة',
            'institution': 'المؤسسة التعليمية',
            'country': 'الدولة',
            'graduation_year': 'سنة التخرج',
            'grade': 'التقدير',
            'certificate_file': 'ملف الشهادة',
        }
        widgets = {
            'certificate_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'


class EmployeeExperienceForm(forms.ModelForm):
    """
    Employee experience form
    نموذج الخبرات العملية
    """
    class Meta:
        model = EmployeeExperience
        fields = ['company_name', 'position', 'start_date', 'end_date', 'is_current', 'responsibilities', 'reason_for_leaving']
        labels = {
            'company_name': 'اسم الشركة',
            'position': 'المنصب',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'is_current': 'الوظيفة الحالية',
            'responsibilities': 'المسؤوليات',
            'reason_for_leaving': 'سبب ترك العمل',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'reason_for_leaving': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }




class EmployeeInsuranceForm(forms.ModelForm):
    """
    Employee insurance form
    نموذج تأمينات الموظف
    """
    class Meta:
        model = EmployeeInsurance
        fields = [
            'insurance_type', 'insurance_number', 'insurance_company',
            'start_date', 'end_date', 'coverage_amount', 'monthly_premium', 'notes'
        ]
        labels = {
            'insurance_type': 'نوع التأمين',
            'insurance_number': 'رقم التأمين',
            'insurance_company': 'شركة التأمين',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'coverage_amount': 'قيمة التغطية',
            'monthly_premium': 'القسط الشهري',
            'notes': 'ملاحظات',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class EmployeeCustodyForm(forms.ModelForm):
    """
    Employee custody form
    نموذج عهد الموظف
    """
    class Meta:
        model = EmployeeCustody
        fields = [
            'custody_type', 'item_name', 'item_description', 'serial_number',
            'item_value', 'issue_date', 'return_date', 'status', 'notes'
        ]
        labels = {
            'custody_type': 'نوع العهدة',
            'item_name': 'اسم الصنف',
            'item_description': 'وصف الصنف',
            'serial_number': 'الرقم التسلسلي',
            'item_value': 'قيمة الصنف',
            'issue_date': 'تاريخ الاستلام',
            'return_date': 'تاريخ الإرجاع',
            'status': 'الحالة',
            'notes': 'ملاحظات',
        }
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'item_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
