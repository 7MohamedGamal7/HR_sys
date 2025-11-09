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
        fields = ['code', 'name_ar', 'name_en', 'parent', 'manager', 'description', 'is_active']
        labels = {
            'code': 'الكود',
            'name_ar': 'الاسم بالعربية',
            'name_en': 'الاسم بالإنجليزية',
            'parent': 'القسم الرئيسي',
            'manager': 'المدير',
            'description': 'الوصف',
            'is_active': 'نشط',
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
                Column('code', css_class='col-md-4'),
                Column('parent', css_class='col-md-4'),
                Column('manager', css_class='col-md-4'),
            ),
            Row(
                Column('name_ar', css_class='col-md-6'),
                Column('name_en', css_class='col-md-6'),
            ),
            'description',
            'is_active',
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
        fields = ['code', 'title_ar', 'title_en', 'department', 'level', 'description', 'is_active']
        labels = {
            'code': 'الكود',
            'title_ar': 'المسمى بالعربية',
            'title_en': 'المسمى بالإنجليزية',
            'department': 'القسم',
            'level': 'المستوى',
            'description': 'الوصف',
            'is_active': 'نشط',
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
        fields = ['code', 'name_ar', 'name_en', 'address', 'city', 'phone', 'email', 'manager', 'is_active']
        labels = {
            'code': 'الكود',
            'name_ar': 'الاسم بالعربية',
            'name_en': 'الاسم بالإنجليزية',
            'address': 'العنوان',
            'city': 'المدينة',
            'phone': 'الهاتف',
            'email': 'البريد الإلكتروني',
            'manager': 'المدير',
            'is_active': 'نشط',
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
            'name', 'start_time', 'end_time', 'break_duration',
            'late_tolerance', 'early_leave_tolerance', 'is_active'
        ]
        labels = {
            'name': 'الاسم',
            'start_time': 'وقت البداية',
            'end_time': 'وقت النهاية',
            'break_duration': 'مدة الاستراحة (دقائق)',
            'late_tolerance': 'التسامح في التأخير (دقائق)',
            'early_leave_tolerance': 'التسامح في المغادرة المبكرة (دقائق)',
            'is_active': 'نشط',
        }
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
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

