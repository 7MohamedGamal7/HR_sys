"""
Forms for reports app
نماذج تطبيق التقارير
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions


class ReportFilterForm(forms.Form):
    """
    Generic report filter form
    نموذج تصفية التقارير العام
    """
    start_date = forms.DateField(
        label='من تاريخ',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='إلى تاريخ',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    department = forms.ModelChoiceField(
        label='القسم',
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    export_format = forms.ChoiceField(
        label='صيغة التصدير',
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from organization.models import Department
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            Row(
                Column('department', css_class='col-md-6'),
                Column('export_format', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'عرض التقرير', css_class='btn btn-primary'),
                HTML('<button type="submit" name="export" value="1" class="btn btn-success">تصدير</button>')
            )
        )


class EmployeeReportFilterForm(forms.Form):
    """
    Employee report filter form
    نموذج تصفية تقرير الموظفين
    """
    employee = forms.ModelChoiceField(
        label='الموظف',
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.ModelChoiceField(
        label='القسم',
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    employment_type = forms.ChoiceField(
        label='نوع التوظيف',
        choices=[('', 'الكل')] + [
            ('full_time', 'دوام كامل'),
            ('part_time', 'دوام جزئي'),
            ('contract', 'عقد'),
            ('temporary', 'مؤقت'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        label='الحالة',
        choices=[
            ('', 'الكل'),
            ('1', 'نشط'),
            ('0', 'غير نشط'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from employees.models import Employee
        from organization.models import Department
        
        self.fields['employee'].queryset = Employee.objects.filter(is_active=True)
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'


class CustomReportForm(forms.Form):
    """
    Custom report builder form
    نموذج إنشاء تقرير مخصص
    """
    report_name = forms.CharField(
        label='اسم التقرير',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    report_type = forms.ChoiceField(
        label='نوع التقرير',
        choices=[
            ('employee', 'الموظفين'),
            ('attendance', 'الحضور'),
            ('leave', 'الإجازات'),
            ('payroll', 'الرواتب'),
            ('performance', 'الأداء'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        label='من تاريخ',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='إلى تاريخ',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fields = forms.MultipleChoiceField(
        label='الحقول',
        choices=[],
        required=True,
        widget=forms.CheckboxSelectMultiple()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

