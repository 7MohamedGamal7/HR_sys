"""
Forms for payroll app
نماذج تطبيق الرواتب
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import Payroll, Payslip, Loan, Bonus


class PayrollForm(forms.ModelForm):
    """
    Payroll form
    نموذج كشف الرواتب
    """
    class Meta:
        model = Payroll
        fields = ['month', 'year', 'status', 'notes']
        labels = {
            'month': 'الشهر',
            'year': 'السنة',
            'status': 'الحالة',
            'notes': 'ملاحظات',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('month', css_class='col-md-4'),
                Column('year', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
            ),
            'notes',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'payroll:payroll_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class PayslipForm(forms.ModelForm):
    """
    Payslip form
    نموذج قسيمة الراتب
    """
    class Meta:
        model = Payslip
        fields = [
            'employee', 'payroll', 'basic_salary', 'housing_allowance',
            'transportation_allowance', 'other_allowances', 'overtime_amount',
            'bonus_amount', 'deductions', 'loan_deduction', 'tax', 'insurance',
            'net_salary', 'payment_date', 'payment_method', 'notes'
        ]
        labels = {
            'employee': 'الموظف',
            'payroll': 'كشف الرواتب',
            'basic_salary': 'الراتب الأساسي',
            'housing_allowance': 'بدل السكن',
            'transportation_allowance': 'بدل المواصلات',
            'other_allowances': 'بدلات أخرى',
            'overtime_amount': 'مبلغ العمل الإضافي',
            'bonus_amount': 'مبلغ المكافأة',
            'deductions': 'الخصومات',
            'loan_deduction': 'خصم القرض',
            'tax': 'الضريبة',
            'insurance': 'التأمين',
            'net_salary': 'صافي الراتب',
            'payment_date': 'تاريخ الدفع',
            'payment_method': 'طريقة الدفع',
            'notes': 'ملاحظات',
        }
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class LoanForm(forms.ModelForm):
    """
    Loan form
    نموذج القرض
    """
    class Meta:
        model = Loan
        fields = [
            'employee', 'amount', 'installments', 'start_date',
            'reason', 'status'
        ]
        labels = {
            'employee': 'الموظف',
            'amount': 'المبلغ',
            'installments': 'عدد الأقساط',
            'start_date': 'تاريخ البداية',
            'reason': 'السبب',
            'status': 'الحالة',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'employee_profile'):
            self.fields['employee'].initial = user.employee_profile
            self.fields['employee'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class BonusForm(forms.ModelForm):
    """
    Bonus form
    نموذج المكافأة
    """
    class Meta:
        model = Bonus
        fields = ['employee', 'amount', 'bonus_type', 'date', 'reason']
        labels = {
            'employee': 'الموظف',
            'amount': 'المبلغ',
            'bonus_type': 'نوع المكافأة',
            'date': 'التاريخ',
            'reason': 'السبب',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

