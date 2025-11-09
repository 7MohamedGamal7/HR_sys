"""
Forms for attendance app
نماذج تطبيق الحضور
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import Attendance, LeaveRequest, Overtime


class AttendanceForm(forms.ModelForm):
    """
    Attendance form
    نموذج الحضور
    """
    class Meta:
        model = Attendance
        fields = [
            'employee', 'date', 'check_in', 'check_out', 'status',
            'late_minutes', 'early_leave_minutes', 'overtime_hours', 'notes'
        ]
        labels = {
            'employee': 'الموظف',
            'date': 'التاريخ',
            'check_in': 'وقت الحضور',
            'check_out': 'وقت الانصراف',
            'status': 'الحالة',
            'late_minutes': 'دقائق التأخير',
            'early_leave_minutes': 'دقائق المغادرة المبكرة',
            'overtime_hours': 'ساعات العمل الإضافي',
            'notes': 'ملاحظات',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            Row(
                Column('check_in', css_class='col-md-6'),
                Column('check_out', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-4'),
                Column('late_minutes', css_class='col-md-4'),
                Column('early_leave_minutes', css_class='col-md-4'),
            ),
            'overtime_hours',
            'notes',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'attendance:attendance_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class LeaveRequestForm(forms.ModelForm):
    """
    Leave request form
    نموذج طلب إجازة
    """
    class Meta:
        model = LeaveRequest
        fields = [
            'employee', 'leave_type', 'start_date', 'end_date',
            'reason', 'attachment'
        ]
        labels = {
            'employee': 'الموظف',
            'leave_type': 'نوع الإجازة',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'reason': 'السبب',
            'attachment': 'مرفق',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user is provided and is an employee, set employee field
        if user and hasattr(user, 'employee_profile'):
            self.fields['employee'].initial = user.employee_profile
            self.fields['employee'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'employee',
            'leave_type',
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            'reason',
            'attachment',
            FormActions(
                Submit('submit', 'تقديم الطلب', css_class='btn btn-primary'),
                HTML('<a href="{% url \'attendance:leave_request_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('تاريخ البداية يجب أن يكون قبل تاريخ النهاية')
        
        return cleaned_data


class LeaveApprovalForm(forms.ModelForm):
    """
    Leave approval form
    نموذج الموافقة على الإجازة
    """
    class Meta:
        model = LeaveRequest
        fields = ['status', 'approved_by_notes']
        labels = {
            'status': 'الحالة',
            'approved_by_notes': 'ملاحظات المدير',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_by_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit status choices to approved/rejected
        self.fields['status'].choices = [
            ('approved', 'موافق عليها'),
            ('rejected', 'مرفوضة'),
        ]
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'status',
            'approved_by_notes',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="javascript:history.back()" class="btn btn-secondary">إلغاء</a>')
            )
        )


class OvertimeForm(forms.ModelForm):
    """
    Overtime form
    نموذج العمل الإضافي
    """
    class Meta:
        model = Overtime
        fields = [
            'employee', 'date', 'hours', 'reason', 'status'
        ]
        labels = {
            'employee': 'الموظف',
            'date': 'التاريخ',
            'hours': 'عدد الساعات',
            'reason': 'السبب',
            'status': 'الحالة',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user is provided and is an employee, set employee field
        if user and hasattr(user, 'employee_profile'):
            self.fields['employee'].initial = user.employee_profile
            self.fields['employee'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'employee',
            Row(
                Column('date', css_class='col-md-6'),
                Column('hours', css_class='col-md-6'),
            ),
            'reason',
            'status',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'attendance:overtime_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class ZKSyncForm(forms.Form):
    """
    ZK device sync form
    نموذج مزامنة أجهزة البصمة
    """
    days = forms.IntegerField(
        label='عدد الأيام للمزامنة',
        required=False,
        initial=7,
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    auto_process = forms.BooleanField(
        label='معالجة تلقائية للسجلات',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'days',
            'auto_process',
            FormActions(
                Submit('submit', 'بدء المزامنة', css_class='btn btn-primary'),
                HTML('<a href="{% url \'attendance:zk_devices\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class AttendanceReportForm(forms.Form):
    """
    Attendance report filter form
    نموذج تصفية تقرير الحضور
    """
    employee = forms.ModelChoiceField(
        label='الموظف',
        queryset=None,
        required=False,
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
    status = forms.ChoiceField(
        label='الحالة',
        required=False,
        choices=[('', 'الكل')] + Attendance.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from employees.models import Employee
        self.fields['employee'].queryset = Employee.objects.filter(is_active=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Row(
                Column('start_date', css_class='col-md-6'),
                Column('end_date', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'عرض التقرير', css_class='btn btn-primary'),
                HTML('<a href="{% url \'attendance:attendance_list\' %}" class="btn btn-secondary">إعادة تعيين</a>')
            )
        )

