"""
Forms for training app
نماذج تطبيق التدريب
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import TrainingProgram, TrainingSession, TrainingEnrollment


class TrainingProgramForm(forms.ModelForm):
    """
    Training program form
    نموذج البرنامج التدريبي
    """
    class Meta:
        model = TrainingProgram
        fields = [
            'name', 'description', 'category', 'duration_hours',
            'max_participants', 'cost', 'is_active'
        ]
        labels = {
            'name': 'الاسم',
            'description': 'الوصف',
            'category': 'الفئة',
            'duration_hours': 'المدة (ساعات)',
            'max_participants': 'الحد الأقصى للمشاركين',
            'cost': 'التكلفة',
            'is_active': 'نشط',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('category', css_class='col-md-6'),
                Column('duration_hours', css_class='col-md-6'),
            ),
            Row(
                Column('max_participants', css_class='col-md-6'),
                Column('cost', css_class='col-md-6'),
            ),
            'is_active',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'training:program_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class TrainingSessionForm(forms.ModelForm):
    """
    Training session form
    نموذج الجلسة التدريبية
    """
    class Meta:
        model = TrainingSession
        fields = [
            'program', 'trainer', 'start_date', 'end_date',
            'location', 'max_participants', 'status'
        ]
        labels = {
            'program': 'البرنامج',
            'trainer': 'المدرب',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'location': 'المكان',
            'max_participants': 'الحد الأقصى للمشاركين',
            'status': 'الحالة',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class TrainingEnrollmentForm(forms.ModelForm):
    """
    Training enrollment form
    نموذج التسجيل في التدريب
    """
    class Meta:
        model = TrainingEnrollment
        fields = ['session', 'employee', 'status', 'completion_date', 'score', 'feedback']
        labels = {
            'session': 'الجلسة',
            'employee': 'الموظف',
            'status': 'الحالة',
            'completion_date': 'تاريخ الإنجاز',
            'score': 'الدرجة',
            'feedback': 'التقييم',
        }
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'employee_profile'):
            self.fields['employee'].initial = user.employee_profile
            self.fields['employee'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'

