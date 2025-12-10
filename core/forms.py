"""
Forms for core app
نماذج تطبيق النواة
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import FormActions
from .models import User, SystemSettings, Notification, CompanySettings


class LoginForm(AuthenticationForm):
    """
    Custom login form with crispy styling
    نموذج تسجيل الدخول المخصص
    """
    username = forms.CharField(
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-signin'
        self.helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('submit', 'تسجيل الدخول', css_class='btn btn-primary btn-block w-100')
            )
        )


class UserRegistrationForm(UserCreationForm):
    """
    User registration form
    نموذج تسجيل مستخدم جديد
    """
    email = forms.EmailField(
        label='البريد الإلكتروني',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'role': 'الدور الوظيفي',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            'role',
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'إنشاء حساب', css_class='btn btn-primary'),
                HTML('<a href="{% url \'core:dashboard\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class UserProfileForm(forms.ModelForm):
    """
    User profile edit form
    نموذج تعديل الملف الشخصي
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'avatar': 'الصورة الشخصية',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            'avatar',
            FormActions(
                Submit('submit', 'حفظ التغييرات', css_class='btn btn-primary'),
                HTML('<a href="{% url \'core:profile\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form
    نموذج تغيير كلمة المرور
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'كلمة المرور الحالية'
        self.fields['new_password1'].label = 'كلمة المرور الجديدة'
        self.fields['new_password2'].label = 'تأكيد كلمة المرور الجديدة'
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            FormActions(
                Submit('submit', 'تغيير كلمة المرور', css_class='btn btn-primary'),
                HTML('<a href="{% url \'core:profile\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class SystemSettingsForm(forms.ModelForm):
    """
    System settings form
    نموذج إعدادات النظام
    """
    class Meta:
        model = SystemSettings
        fields = ['key', 'value', 'description', 'category']
        labels = {
            'key': 'المفتاح',
            'value': 'القيمة',
            'description': 'الوصف',
            'category': 'الفئة',
        }
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'key',
            'value',
            'description',
            'category',
            FormActions(
                Submit('submit', 'حفظ', css_class='btn btn-primary'),
                HTML('<a href="{% url \'core:system_settings\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class NotificationForm(forms.ModelForm):
    """
    Notification form
    نموذج الإشعارات
    """
    class Meta:
        model = Notification
        fields = ['user', 'title', 'message', 'notification_type', 'link']
        labels = {
            'user': 'المستخدم',
            'title': 'العنوان',
            'message': 'الرسالة',
            'notification_type': 'نوع الإشعار',
            'link': 'الرابط',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'user',
            'title',
            'message',
            Row(
                Column('notification_type', css_class='col-md-6'),
                Column('link', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'إرسال الإشعار', css_class='btn btn-primary'),
                HTML('<a href="{% url \'core:notifications\' %}" class="btn btn-secondary">إلغاء</a>')
            )
        )


class DateRangeFilterForm(forms.Form):
    """
    Date range filter form for reports
    نموذج تصفية حسب نطاق التاريخ
    """
    start_date = forms.DateField(
        label='من تاريخ',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        label='إلى تاريخ',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='col-md-5'),
                Column('end_date', css_class='col-md-5'),
                Column(
                    Submit('submit', 'تصفية', css_class='btn btn-primary'),
                    css_class='col-md-2'
                ),
            )
        )


class CompanySettingsForm(forms.ModelForm):
    """
    Comprehensive company settings form
    نموذج إعدادات الشركة الشامل
    """
    class Meta:
        model = CompanySettings
        exclude = ['updated_at', 'updated_by']
        widgets = {
            'company_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'theme_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'

