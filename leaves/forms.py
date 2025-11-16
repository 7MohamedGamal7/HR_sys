"""
Forms for leaves app
نماذج تطبيق الإجازات
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import LeavePolicy, LeaveBalance, LeaveApprovalWorkflow


class LeavePolicyForm(forms.ModelForm):
    """
    Leave policy form
    نموذج سياسة الإجازات
    """
    class Meta:
        model = LeavePolicy
        fields = [
            'name', 'leave_type', 'days_per_year', 'max_consecutive_days',
            'requires_approval', 'is_paid', 'carry_forward', 'description'
        ]
        labels = {
            'name': 'الاسم',
            'leave_type': 'نوع الإجازة',
            'days_per_year': 'الأيام في السنة',
            'max_consecutive_days': 'الحد الأقصى للأيام المتتالية',
            'requires_approval': 'تتطلب موافقة',
            'is_paid': 'مدفوعة',
            'carry_forward': 'يمكن ترحيلها',
            'description': 'الوصف',
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
                Column('name', css_class='col-md-6'),
                Column('leave_type', css_class='col-md-6'),
            ),
            Row(
                Column('days_per_year', css_class='col-md-6'),
                Column('max_consecutive_days', css_class='col-md-6'),
            ),
            Row(
                Column('requires_approval', css_class='col-md-4'),
                Column('is_paid', css_class='col-md-4'),
                Column('carry_forward', css_class='col-md-4'),
            ),
            'description',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'leaves:leave_policy_list\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class LeaveBalanceForm(forms.ModelForm):
    """
    Leave balance form
    نموذج رصيد الإجازات
    """
    class Meta:
        model = LeaveBalance
        fields = ['employee', 'leave_type', 'year', 'total_days', 'used_days']
        labels = {
            'employee': 'الموظف',
            'leave_type': 'نوع الإجازة',
            'year': 'السنة',
            'total_days': 'إجمالي الأيام',
            'used_days': 'الأيام المستخدمة',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class LeaveApprovalWorkflowForm(forms.ModelForm):
    """
    Leave approval workflow form
    نموذج سير عمل الموافقة على الإجازات
    """
    class Meta:
        model = LeaveApprovalWorkflow
        fields = ['leave_request', 'approver', 'level', 'status', 'comments']
        labels = {
            'leave_request': 'طلب الإجازة',
            'approver': 'المعتمد',
            'level': 'المستوى',
            'status': 'الحالة',
            'comments': 'التعليقات',
        }
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

