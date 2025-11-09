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
    today = timezone.now().date()
    
    # Statistics
    total_employees = Employee.objects.filter(is_active=True).count()
    present_today = Attendance.objects.filter(
        date=today,
        status__in=['present', 'late']
    ).count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    total_departments = Department.objects.filter(is_active=True).count()
    
    # Recent attendance (last 10)
    recent_attendance = Attendance.objects.select_related('employee').filter(
        date=today
    ).order_by('-check_in')[:10]
    
    # Pending leave requests (last 10)
    pending_leave_requests = LeaveRequest.objects.select_related('employee').filter(
        status='pending'
    ).order_by('-created_at')[:10]
    
    # Upcoming birthdays (next 30 days)
    upcoming_birthdays = Employee.objects.filter(
        is_active=True,
        date_of_birth__isnull=False
    ).extra(
        select={
            'birthday_this_year': "DATEADD(year, DATEDIFF(year, date_of_birth, GETDATE()), date_of_birth)"
        }
    )[:5]
    
    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'pending_leaves': pending_leaves,
        'total_departments': total_departments,
        'recent_attendance': recent_attendance,
        'pending_leave_requests': pending_leave_requests,
        'upcoming_birthdays': upcoming_birthdays,
    }
    
    return render(request, 'core/dashboard.html', context)


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
    
    settings, created = SystemSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث إعدادات النظام بنجاح.')
            return redirect('core:system_settings')
    else:
        form = SystemSettingsForm(instance=settings)
    
    return render(request, 'core/system_settings.html', {'form': form})


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

