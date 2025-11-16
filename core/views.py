"""
Views for core app
عرض تطبيق النواة
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, Notification, SystemSettings
from .forms import LoginForm, UserProfileForm, CustomPasswordChangeForm, SystemSettingsForm
from employees.models import Employee
from attendance.models import Attendance, LeaveRequest
from organization.models import Department


def login_view(request):
    """
    User login view
    عرض تسجيل الدخول
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً {user.get_full_name() or user.username}!')
                return redirect('core:dashboard')
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view
    عرض تسجيل الخروج
    """
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('core:login')


@login_required
def dashboard(request):
    """
    Dashboard view
    عرض لوحة التحكم
    """
    try:
        today = timezone.now().date()

        # Statistics
        total_employees = Employee.objects.filter(is_active=True).count()

        try:
            present_today = Attendance.objects.filter(
                date=today,
                status__in=['present', 'late']
            ).count()
        except:
            present_today = 0

        try:
            pending_leaves = LeaveRequest.objects.filter(status='pending').count()
        except:
            pending_leaves = 0

        try:
            total_departments = Department.objects.filter(is_active=True).count()
        except:
            total_departments = 0

        context = {
            'total_employees': total_employees,
            'present_today': present_today,
            'pending_leaves': pending_leaves,
            'total_departments': total_departments,
        }
    except Exception as e:
        context = {
            'total_employees': 0,
            'present_today': 0,
            'pending_leaves': 0,
            'total_departments': 0,
        }

    return render(request, 'core/dashboard_simple.html', context)


@login_required
def profile_view(request):
    """
    User profile view
    عرض الملف الشخصي
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح.')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'core/profile.html', {'form': form})


@login_required
def change_password(request):
    """
    Change password view
    عرض تغيير كلمة المرور
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'تم تغيير كلمة المرور بنجاح.')
            return redirect('core:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'core/change_password.html', {'form': form})


@login_required
def notifications_list(request):
    """
    Notifications list view
    عرض قائمة الإشعارات
    """
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    # Mark as read
    if request.GET.get('mark_read'):
        notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, 'تم تحديد جميع الإشعارات كمقروءة.')
        return redirect('core:notifications_list')
    
    context = {
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count(),
    }
    
    return render(request, 'core/notifications_list.html', context)


@login_required
def notification_detail(request, pk):
    """
    Notification detail view
    عرض تفاصيل الإشعار
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    # Mark as read
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    
    return render(request, 'core/notification_detail.html', {'notification': notification})


@login_required
def system_settings(request):
    """
    System settings view
    عرض إعدادات النظام
    """
    # Only admin can access
    if not request.user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية للوصول إلى هذه الصفحة.')
        return redirect('core:dashboard')

    from .models import CompanySettings
    from .forms import CompanySettingsForm
    from django.db import connection

    # Load singleton settings
    settings = CompanySettings.load()

    # Get database info
    db_name = connection.settings_dict.get('NAME', 'Unknown')
    db_engine = connection.settings_dict.get('ENGINE', 'Unknown')

    if request.method == 'POST':
        form = CompanySettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.updated_by = request.user
            settings.save()
            messages.success(request, 'تم تحديث إعدادات النظام بنجاح.')
            return redirect('core:system_settings')
    else:
        form = CompanySettingsForm(instance=settings)

    context = {
        'form': form,
        'settings': settings,
        'db_name': db_name,
        'db_engine': 'MS SQL Server' if 'mssql' in db_engine else db_engine,
    }

    return render(request, 'core/system_settings.html', context)


@login_required
def mark_notification_read(request, pk):
    """
    Mark notification as read
    تحديد الإشعار كمقروء
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('core:notifications_list')


@login_required
def delete_notification(request, pk):
    """
    Delete notification
    حذف الإشعار
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'تم حذف الإشعار بنجاح.')
    
    return redirect('core:notifications_list')

