"""
Views for attendance app
عرض تطبيق الحضور
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Attendance, LeaveRequest, Overtime
from .forms import AttendanceForm, LeaveRequestForm, LeaveApprovalForm, OvertimeForm, ZKSyncForm, AttendanceReportForm
from .zk_integration import sync_all_devices, test_device_connection, get_sync_status
from employees.models import Employee


@login_required
def attendance_today(request):
    """
    Today's attendance view
    عرض حضور اليوم
    """
    today = timezone.now().date()
    attendances = Attendance.objects.select_related('employee').filter(date=today).order_by('-check_in')
    
    # Statistics
    total = attendances.count()
    present = attendances.filter(status__in=['present', 'late']).count()
    late = attendances.filter(status='late').count()
    absent = Employee.objects.filter(is_active=True).count() - present
    
    context = {
        'attendances': attendances,
        'today': today,
        'total': total,
        'present': present,
        'late': late,
        'absent': absent,
    }
    
    return render(request, 'attendance/attendance_today.html', context)


@login_required
def attendance_list(request):
    """
    Attendance list view
    عرض قائمة الحضور
    """
    attendances = Attendance.objects.select_related('employee').all()
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
    
    # Filter by employee
    employee_id = request.GET.get('employee')
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        attendances = attendances.filter(status=status)
    
    # Order by date descending
    attendances = attendances.order_by('-date', '-check_in')
    
    # Pagination
    paginator = Paginator(attendances, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def attendance_detail(request, pk):
    """
    Attendance detail view
    عرض تفاصيل الحضور
    """
    attendance = get_object_or_404(Attendance, pk=pk)
    return render(request, 'attendance/attendance_detail.html', {'attendance': attendance})


@login_required
def attendance_create(request):
    """
    Manual attendance create view
    عرض إضافة حضور يدوي
    """
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'تم إضافة سجل الحضور بنجاح.')
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'attendance/attendance_form.html', {'form': form})


# Leave Request Views
@login_required
def leave_request_list(request):
    """
    Leave request list view
    عرض قائمة طلبات الإجازات
    """
    leave_requests = LeaveRequest.objects.select_related('employee').all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        leave_requests = leave_requests.filter(status=status)
    
    # Order by created date descending
    leave_requests = leave_requests.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(leave_requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'attendance/leave_request_list.html', context)


@login_required
def my_leave_requests(request):
    """
    My leave requests view
    عرض إجازاتي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    leave_requests = LeaveRequest.objects.filter(
        employee=request.user.employee_profile
    ).order_by('-created_at')
    
    context = {
        'leave_requests': leave_requests,
    }
    
    return render(request, 'attendance/my_leave_requests.html', context)


@login_required
def leave_request_detail(request, pk):
    """
    Leave request detail view
    عرض تفاصيل طلب الإجازة
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    return render(request, 'attendance/leave_request_detail.html', {'leave_request': leave_request})


@login_required
def leave_request_create(request):
    """
    Leave request create view
    عرض إضافة طلب إجازة
    """
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, user=request.user)
        if form.is_valid():
            leave_request = form.save()
            messages.success(request, 'تم إرسال طلب الإجازة بنجاح.')
            return redirect('attendance:my_leave_requests')
    else:
        form = LeaveRequestForm(user=request.user)
    
    return render(request, 'attendance/leave_request_form.html', {'form': form})


@login_required
def leave_request_approve(request, pk):
    """
    Leave request approve view
    عرض الموافقة على طلب الإجازة
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.approved_by = request.user
            leave_request.approved_at = timezone.now()
            leave_request.status = 'approved'
            leave_request.save()
            messages.success(request, 'تمت الموافقة على طلب الإجازة بنجاح.')
            return redirect('attendance:leave_request_list')
    else:
        form = LeaveApprovalForm(instance=leave_request)
    
    return render(request, 'attendance/leave_request_approve.html', {'form': form, 'leave_request': leave_request})


@login_required
def leave_request_reject(request, pk):
    """
    Leave request reject view
    عرض رفض طلب الإجازة
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        leave_request.status = 'rejected'
        leave_request.rejection_reason = rejection_reason
        leave_request.approved_by = request.user
        leave_request.approved_at = timezone.now()
        leave_request.save()
        messages.success(request, 'تم رفض طلب الإجازة.')
        return redirect('attendance:leave_request_list')
    
    return render(request, 'attendance/leave_request_reject.html', {'leave_request': leave_request})


# Overtime Views
@login_required
def overtime_list(request):
    """
    Overtime list view
    عرض قائمة العمل الإضافي
    """
    overtimes = Overtime.objects.select_related('employee').all().order_by('-date')
    
    # Pagination
    paginator = Paginator(overtimes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'attendance/overtime_list.html', context)


@login_required
def overtime_create(request):
    """
    Overtime create view
    عرض إضافة عمل إضافي
    """
    if request.method == 'POST':
        form = OvertimeForm(request.POST)
        if form.is_valid():
            overtime = form.save()
            messages.success(request, 'تم إضافة سجل العمل الإضافي بنجاح.')
            return redirect('attendance:overtime_list')
    else:
        form = OvertimeForm()
    
    return render(request, 'attendance/overtime_form.html', {'form': form})


# ZK Device Sync Views
@login_required
def zk_sync(request):
    """
    ZK device sync view
    عرض مزامنة أجهزة البصمة
    """
    if request.method == 'POST':
        form = ZKSyncForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data.get('days', 1)
            auto_process = form.cleaned_data.get('auto_process', True)
            
            try:
                result = sync_all_devices(days=days, auto_process=auto_process)
                messages.success(request, f'تمت المزامنة بنجاح. تم جلب {result.get("total_synced", 0)} سجل.')
                return redirect('attendance:zk_sync')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء المزامنة: {str(e)}')
    else:
        form = ZKSyncForm()
    
    # Get sync status
    sync_status = get_sync_status()
    
    context = {
        'form': form,
        'sync_status': sync_status,
    }
    
    return render(request, 'attendance/zk_sync.html', context)


@login_required
def zk_test_connection(request):
    """
    Test ZK device connection (AJAX)
    اختبار اتصال جهاز البصمة
    """
    device_ip = request.GET.get('device_ip')
    
    if not device_ip:
        return JsonResponse({'success': False, 'message': 'عنوان IP مطلوب'})
    
    try:
        result = test_device_connection(device_ip)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

