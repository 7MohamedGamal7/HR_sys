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
            'emp_code', 'first_name_ar', 'middle_name_ar', 'last_name_ar',
            'first_name_en', 'last_name_en', 'national_id', 'passport_number',
            'date_of_birth', 'gender', 'marital_status', 'nationality', 'religion',
            'email', 'phone', 'mobile', 'address', 'city', 'postal_code',
            'department', 'position', 'branch', 'manager', 'hire_date', 'employment_type',
            'work_shift', 'probation_end_date', 'confirmation_date',
            'basic_salary', 'housing_allowance', 'transport_allowance', 'other_allowances',
            'annual_leave_balance', 'sick_leave_balance',
            'bank_name', 'bank_account_number', 'iban',
            'photo', 'zk_user_id', 'is_active', 'termination_date', 'termination_reason'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'probation_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'termination_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'termination_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    'المعلومات الشخصية',
                    Row(
                        Column('emp_code', css_class='col-md-4'),
                        Column('photo', css_class='col-md-8'),
                    ),
                    Row(
                        Column('first_name_ar', css_class='col-md-6'),
                        Column('last_name_ar', css_class='col-md-6'),
                    ),
                    Row(
                        Column('first_name_en', css_class='col-md-6'),
                        Column('last_name_en', css_class='col-md-6'),
                    ),
                    Row(
                        Column('national_id', css_class='col-md-6'),
                        Column('passport_number', css_class='col-md-6'),
                    ),
                    Row(
                        Column('date_of_birth', css_class='col-md-4'),
                        Column('gender', css_class='col-md-4'),
                        Column('marital_status', css_class='col-md-4'),
                    ),
                    Row(
                        Column('nationality', css_class='col-md-6'),
                        Column('religion', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'معلومات الاتصال',
                    Row(
                        Column('email', css_class='col-md-6'),
                        Column('phone', css_class='col-md-6'),
                    ),
                    Row(
                        Column('mobile', css_class='col-md-6'),
                    ),
                    'address',
                ),
                Tab(
                    'معلومات الوظيفة',
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
                        Column('work_shift', css_class='col-md-4'),
                    ),
                    'probation_end_date',
                    'zk_user_id',
                ),
                Tab(
                    'معلومات الراتب',
                    Row(
                        Column('basic_salary', css_class='col-md-6'),
                        Column('housing_allowance', css_class='col-md-6'),
                    ),
                    Row(
                        Column('transport_allowance', css_class='col-md-6'),
                        Column('other_allowances', css_class='col-md-6'),
                    ),
                ),
                Tab(
                    'المعلومات البنكية',
                    'bank_name',
                    Row(
                        Column('bank_account_number', css_class='col-md-6'),
                        Column('iban', css_class='col-md-6'),
                    ),
                ),
            ),
            'is_active',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'employees:employee_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


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
