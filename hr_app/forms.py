from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import TblEmployees, TblLeaves, TblSettings


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['remember_me'].widget.attrs.update({'class': 'form-check-input'})


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = TblEmployees
        fields = [
            'emp_code', 'emp_fullname', 'national_id', 'job_title', 'department',
            'hire_date', 'salary_basic', 'salary_housing', 'salary_transport',
            'salary_other', 'allowed_annual_leaves', 'allowed_sick_leaves',
            'allowed_casual_leaves', 'work_start', 'work_end', 'telegram_userid',
            'is_active'
        ]
        widgets = {
            'emp_code': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_basic': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_housing': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_transport': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_other': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'allowed_annual_leaves': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowed_sick_leaves': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowed_casual_leaves': forms.NumberInput(attrs={'class': 'form-control'}),
            'work_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'work_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'telegram_userid': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make emp_code required
        self.fields['emp_code'].required = True
        self.fields['emp_fullname'].required = True
    
    def save(self, commit=True):
        # Calculate salary_total before saving
        instance = super().save(commit=False)
        
        # Calculate the total salary from component parts
        basic = instance.salary_basic or 0
        housing = instance.salary_housing or 0
        transport = instance.salary_transport or 0
        other = instance.salary_other or 0
        instance.salary_total = basic + housing + transport + other
        
        if commit:
            # Save without including Salary_Total in the SQL statement
            instance.save(update_fields=[
                'emp_code', 'emp_fullname', 'national_id', 'job_title', 'department',
                'hire_date', 'salary_basic', 'salary_housing', 'salary_transport',
                'salary_other', 'allowed_annual_leaves', 'allowed_sick_leaves',
                'allowed_casual_leaves', 'work_start', 'work_end', 'telegram_userid',
                'is_active'
            ])
        return instance


class LeaveForm(forms.ModelForm):
    class Meta:
        model = TblLeaves
        fields = ['emp', 'start_date', 'end_date', 'leave_type']
        widgets = {
            'emp': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Annual', 'إجازة سنوية'),
                ('Sick', 'إجازة مرضية'),
                ('Casual', 'إجازة عارضة'),
                ('Maternity', 'إجازة أمومة'),
                ('Paternity', 'إجازة أبوة'),
                ('Unpaid', 'إجازة غير مدفوعة'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emp'].queryset = TblEmployees.objects.filter(is_active=True)
        self.fields['emp'].required = True
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['leave_type'].required = True


class SettingsForm(forms.ModelForm):
    class Meta:
        model = TblSettings
        fields = [
            'company_name', 'workday_start', 'workday_end', 'lunch_break_minutes',
            'late_threshold_min', 'overtime_rate', 'monthly_working_hours', 'salary_currency'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'workday_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'workday_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'lunch_break_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'late_threshold_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'overtime_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monthly_working_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_currency': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('USD', 'USD ($)'),
                ('EUR', 'EUR (€)'),
                ('GBP', 'GBP (£)'),
                ('EGP', 'EGP (E£)'),
            ]),
        }