"""
Forms for recruitment app
نماذج تطبيق التوظيف
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import FormActions
from .models import JobPosting, JobApplication, Interview, JobOffer


class JobPostingForm(forms.ModelForm):
    """
    Job posting form
    نموذج إعلان الوظيفة
    """
    class Meta:
        model = JobPosting
        fields = [
            'title', 'department', 'position', 'vacancies',
            'salary_range_min', 'salary_range_max', 'description', 'requirements',
            'responsibilities', 'posting_date', 'closing_date', 'status'
        ]
        labels = {
            'title': 'المسمى الوظيفي',
            'department': 'القسم',
            'position': 'المنصب',
            'vacancies': 'عدد الشواغر',
            'salary_range_min': 'الحد الأدنى للراتب',
            'salary_range_max': 'الحد الأقصى للراتب',
            'description': 'الوصف الوظيفي',
            'requirements': 'المتطلبات',
            'responsibilities': 'المسؤوليات',
            'posting_date': 'تاريخ النشر',
            'closing_date': 'تاريخ الإغلاق',
            'status': 'الحالة',
        }
        widgets = {
            'posting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'closing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class ApplicationForm(forms.ModelForm):
    """
    Application form
    نموذج التقديم
    """
    class Meta:
        model = JobApplication
        fields = [
            'job_posting', 'applicant_name', 'email', 'phone',
            'resume', 'cover_letter', 'status'
        ]
        labels = {
            'job_posting': 'الوظيفة',
            'applicant_name': 'اسم المتقدم',
            'email': 'البريد الإلكتروني',
            'phone': 'الهاتف',
            'resume': 'السيرة الذاتية',
            'cover_letter': 'خطاب التقديم',
            'status': 'الحالة',
        }
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class InterviewForm(forms.ModelForm):
    """
    Interview form
    نموذج المقابلة
    """
    class Meta:
        model = Interview
        fields = [
            'application', 'interview_date', 'location',
            'interviewer', 'status', 'result', 'feedback'
        ]
        labels = {
            'application': 'طلب التوظيف',
            'interview_date': 'تاريخ ووقت المقابلة',
            'location': 'المكان',
            'interviewer': 'المقابل',
            'status': 'الحالة',
            'result': 'النتيجة',
            'feedback': 'التغذية الراجعة',
        }
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class JobOfferForm(forms.ModelForm):
    """
    Job offer form
    نموذج عرض العمل
    """
    class Meta:
        model = JobOffer
        fields = [
            'application', 'position', 'salary', 'start_date',
            'offer_letter', 'status'
        ]
        labels = {
            'application': 'الطلب',
            'position': 'المنصب',
            'salary': 'الراتب',
            'start_date': 'تاريخ البداية',
            'offer_letter': 'خطاب العرض',
            'status': 'الحالة',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'offer_letter': forms.FileInput(attrs={'class': 'form-control'}),
        }

