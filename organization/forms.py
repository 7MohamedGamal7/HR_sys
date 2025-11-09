"""
Forms for organization app
نماذج تطبيق الهيكل التنظيمي
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import Department, Position, Branch, WorkShift, Holiday


class DepartmentForm(forms.ModelForm):
    """
    Department form
    نموذج القسم
    """
    class Meta:
        model = Department
        fields = ['dept_code', 'dept_name_ar', 'dept_name_en', 'parent_department', 'manager', 'description', 'location', 'phone', 'email']
        labels = {
            'dept_code': 'رمز القسم',
            'dept_name_ar': 'اسم القسم بالعربية',
            'dept_name_en': 'اسم القسم بالإنجليزية',
            'parent_department': 'القسم الرئيسي',
            'manager': 'المدير',
            'description': 'الوصف',
            'location': 'الموقع',
            'phone': 'الهاتف',
            'email': 'البريد الإلكتروني',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('dept_code', css_class='col-md-4'),
                Column('parent_department', css_class='col-md-4'),
                Column('manager', css_class='col-md-4'),
            ),
            Row(
                Column('dept_name_ar', css_class='col-md-6'),
                Column('dept_name_en', css_class='col-md-6'),
            ),
            'description',
            Row(
                Column('location', css_class='col-md-4'),
                Column('phone', css_class='col-md-4'),
                Column('email', css_class='col-md-4'),
            ),
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'organization:department_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class PositionForm(forms.ModelForm):
    """
    Position form
    نموذج المنصب
    """
    class Meta:
        model = Position
        fields = ['position_code', 'position_name_ar', 'position_name_en', 'department', 'level', 'description', 'min_salary', 'max_salary']
        labels = {
            'position_code': 'رمز المنصب',
            'position_name_ar': 'اسم المنصب بالعربية',
            'position_name_en': 'اسم المنصب بالإنجليزية',
            'department': 'القسم',
            'level': 'المستوى',
            'description': 'الوصف',
            'min_salary': 'الحد الأدنى للراتب',
            'max_salary': 'الحد الأقصى للراتب',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class BranchForm(forms.ModelForm):
    """
    Branch form
    نموذج الفرع
    """
    class Meta:
        model = Branch
        fields = ['branch_code', 'branch_name_ar', 'branch_name_en', 'address', 'city', 'phone', 'email', 'manager']
        labels = {
            'branch_code': 'رمز الفرع',
            'branch_name_ar': 'اسم الفرع بالعربية',
            'branch_name_en': 'اسم الفرع بالإنجليزية',
            'address': 'العنوان',
            'city': 'المدينة',
            'phone': 'الهاتف',
            'email': 'البريد الإلكتروني',
            'manager': 'المدير',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class WorkShiftForm(forms.ModelForm):
    """
    Work shift form
    نموذج الوردية
    """
    class Meta:
        model = WorkShift
        fields = [
            'shift_name', 'start_time', 'end_time', 'break_duration',
            'working_hours', 'description'
        ]
        labels = {
            'shift_name': 'اسم الوردية',
            'start_time': 'وقت البداية',
            'end_time': 'وقت النهاية',
            'break_duration': 'مدة الاستراحة (دقائق)',
            'working_hours': 'ساعات العمل',
            'description': 'الوصف',
        }
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class HolidayForm(forms.ModelForm):
    """
    Holiday form
    نموذج العطلة
    """
    class Meta:
        model = Holiday
        fields = ['name', 'date', 'holiday_type', 'is_recurring', 'description']
        labels = {
            'name': 'الاسم',
            'date': 'التاريخ',
            'holiday_type': 'نوع العطلة',
            'is_recurring': 'متكررة سنوياً',
            'description': 'الوصف',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

