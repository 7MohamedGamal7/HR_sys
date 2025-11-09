"""
Admin configuration for employees app
"""
from django.contrib import admin
from .models import (
    Employee, EmployeeDocument, EmployeeContract,
    EmergencyContact, EmployeeEducation, EmployeeExperience
)


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 0
    fields = ['document_type', 'document_name', 'document_file', 'issue_date', 'expiry_date']


class EmployeeContractInline(admin.TabularInline):
    model = EmployeeContract
    extra = 0
    fields = ['contract_type', 'contract_number', 'start_date', 'end_date', 'salary', 'is_current']


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 0
    fields = ['name', 'relationship', 'phone', 'mobile', 'is_primary']


class EmployeeEducationInline(admin.TabularInline):
    model = EmployeeEducation
    extra = 0
    fields = ['degree', 'field_of_study', 'institution', 'graduation_year']


class EmployeeExperienceInline(admin.TabularInline):
    model = EmployeeExperience
    extra = 0
    fields = ['company_name', 'position', 'start_date', 'end_date', 'is_current']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Employee Admin"""
    list_display = [
        'emp_code', 'get_full_name_ar', 'department', 'position',
        'email', 'phone', 'hire_date', 'is_active'
    ]
    list_filter = [
        'is_active', 'department', 'position', 'employment_type',
        'gender', 'marital_status', 'hire_date'
    ]
    search_fields = [
        'emp_code', 'first_name_ar', 'last_name_ar',
        'first_name_en', 'last_name_en', 'national_id',
        'email', 'phone'
    ]
    ordering = ['emp_code']
    date_hierarchy = 'hire_date'
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                'emp_code', 'first_name_ar', 'middle_name_ar', 'last_name_ar',
                'first_name_en', 'last_name_en', 'photo'
            )
        }),
        ('المعلومات الشخصية', {
            'fields': (
                'national_id', 'passport_number', 'date_of_birth',
                'gender', 'marital_status', 'nationality', 'religion'
            )
        }),
        ('معلومات الاتصال', {
            'fields': (
                'email', 'phone', 'mobile', 'address', 'city', 'postal_code'
            )
        }),
        ('معلومات التوظيف', {
            'fields': (
                'department', 'position', 'branch', 'manager',
                'employment_type', 'hire_date', 'probation_end_date',
                'confirmation_date', 'work_shift'
            )
        }),
        ('معلومات الراتب', {
            'fields': (
                'basic_salary', 'housing_allowance', 'transport_allowance',
                'other_allowances'
            )
        }),
        ('أرصدة الإجازات', {
            'fields': (
                'annual_leave_balance', 'sick_leave_balance'
            )
        }),
        ('المعلومات البنكية', {
            'fields': (
                'bank_name', 'bank_account_number', 'iban'
            )
        }),
        ('الحالة', {
            'fields': (
                'is_active', 'termination_date', 'termination_reason'
            )
        }),
        ('جهاز البصمة', {
            'fields': ('zk_user_id',)
        }),
    )
    
    # inlines = [
    #     EmployeeDocumentInline,
    #     EmployeeContractInline,
    #     EmergencyContactInline,
    #     EmployeeEducationInline,
    #     EmployeeExperienceInline,
    # ]


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    """Employee Document Admin"""
    list_display = ['employee', 'document_type', 'document_name', 'issue_date', 'expiry_date']
    list_filter = ['document_type', 'issue_date', 'expiry_date']
    search_fields = ['employee__emp_code', 'document_name']
    ordering = ['-created_at']


@admin.register(EmployeeContract)
class EmployeeContractAdmin(admin.ModelAdmin):
    """Employee Contract Admin"""
    list_display = ['employee', 'contract_number', 'contract_type', 'start_date', 'end_date', 'is_current']
    list_filter = ['contract_type', 'is_current', 'start_date']
    search_fields = ['employee__emp_code', 'contract_number']
    ordering = ['-start_date']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Emergency Contact Admin"""
    list_display = ['employee', 'name', 'relationship', 'phone', 'is_primary']
    list_filter = ['relationship', 'is_primary']
    search_fields = ['employee__emp_code', 'name', 'phone']


@admin.register(EmployeeEducation)
class EmployeeEducationAdmin(admin.ModelAdmin):
    """Employee Education Admin"""
    list_display = ['employee', 'degree', 'field_of_study', 'institution', 'graduation_year']
    list_filter = ['degree', 'graduation_year']
    search_fields = ['employee__emp_code', 'field_of_study', 'institution']
    ordering = ['-graduation_year']


@admin.register(EmployeeExperience)
class EmployeeExperienceAdmin(admin.ModelAdmin):
    """Employee Experience Admin"""
    list_display = ['employee', 'company_name', 'position', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['employee__emp_code', 'company_name', 'position']
    ordering = ['-start_date']

