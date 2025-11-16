"""
Forms for training app
نماذج تطبيق التدريب
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import TrainingProgram, TrainingEnrollment


class TrainingProgramForm(forms.ModelForm):
    """
    Training program form
    نموذج البرنامج التدريبي
    """
    class Meta:
        model = TrainingProgram
        fields = [
            'name', 'description', 'objectives', 'duration_hours', 'start_date', 'end_date',
            'trainer', 'location', 'max_participants', 'cost', 'status'
        ]
        labels = {
            'name': 'اسم البرنامج',
            'description': 'الوصف',
            'objectives': 'الأهداف',
            'duration_hours': 'المدة (ساعات)',
            'start_date': 'تاريخ البداية',
            'end_date': 'تاريخ النهاية',
            'trainer': 'المدرب',
            'location': 'المكان',
            'max_participants': 'الحد الأقصى للمشاركين',
            'cost': 'التكلفة',
            'status': 'الحالة',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'objectives': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
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
        fields = ['employee', 'training_program', 'status', 'attendance_percentage', 'final_score', 'feedback', 'certificate_issued']
        labels = {
            'employee': 'الموظف',
            'training_program': 'البرنامج التدريبي',
            'status': 'الحالة',
            'attendance_percentage': 'نسبة الحضور',
            'final_score': 'الدرجة النهائية',
            'feedback': 'الملاحظات',
            'certificate_issued': 'تم إصدار الشهادة',
        }
        widgets = {
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

