"""
Forms for performance app
نماذج تطبيق تقييم الأداء
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import PerformanceReview, KPI, Goal


class PerformanceReviewForm(forms.ModelForm):
    """
    Performance review form
    نموذج تقييم الأداء
    """
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'review_cycle', 'reviewer', 'review_date',
            'overall_rating', 'strengths', 'weaknesses', 'recommendations', 'status'
        ]
        labels = {
            'employee': 'الموظف',
            'review_cycle': 'دورة التقييم',
            'reviewer': 'المقيّم',
            'review_date': 'تاريخ التقييم',
            'overall_rating': 'التقييم الإجمالي',
            'strengths': 'نقاط القوة',
            'weaknesses': 'نقاط الضعف',
            'recommendations': 'التوصيات',
            'status': 'الحالة',
        }
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'strengths': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'weaknesses': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'recommendations': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class KPIForm(forms.ModelForm):
    """
    KPI form
    نموذج مؤشر الأداء الرئيسي
    """
    class Meta:
        model = KPI
        fields = ['name', 'description', 'measurement_unit', 'target_value', 'weight', 'is_active']
        labels = {
            'name': 'الاسم',
            'description': 'الوصف',
            'measurement_unit': 'وحدة القياس',
            'target_value': 'القيمة المستهدفة',
            'weight': 'الوزن',
            'is_active': 'نشط',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class GoalForm(forms.ModelForm):
    """
    Goal form
    نموذج الهدف
    """
    class Meta:
        model = Goal
        fields = [
            'employee', 'title', 'description', 'start_date', 'due_date',
            'priority', 'status', 'progress'
        ]
        labels = {
            'employee': 'الموظف',
            'title': 'العنوان',
            'description': 'الوصف',
            'start_date': 'تاريخ البداية',
            'due_date': 'تاريخ الاستحقاق',
            'priority': 'الأولوية',
            'status': 'الحالة',
            'progress': 'التقدم (%)',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'employee_profile'):
            self.fields['employee'].initial = user.employee_profile
            self.fields['employee'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'

