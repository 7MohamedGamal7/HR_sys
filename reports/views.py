"""
Views for reports app
عرض تطبيق التقارير
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from employees.models import Employee
from attendance.models import Attendance, LeaveRequest
from payroll.models import Payroll, Payslip
from organization.models import Department
from .forms import ReportFilterForm, EmployeeReportFilterForm


@login_required
def reports_dashboard(request):
    """
    Reports dashboard view
    عرض لوحة التقارير
    """
    context = {
        'title': 'لوحة التقارير',
    }
    
    return render(request, 'reports/reports_dashboard.html', context)


@login_required
def employee_summary_report(request):
    """
    Employee summary report view
    عرض تقرير ملخص الموظفين
    """
    employees = Employee.objects.filter(is_active=True)
    
    # Apply filters
    if request.method == 'GET':
        form = EmployeeReportFilterForm(request.GET)
        if form.is_valid():
            employee = form.cleaned_data.get('employee')
            department = form.cleaned_data.get('department')
            employment_type = form.cleaned_data.get('employment_type')
            is_active = form.cleaned_data.get('is_active')
            
            if employee:
                employees = employees.filter(id=employee.id)
            if department:
                employees = employees.filter(department=department)
            if employment_type:
                employees = employees.filter(employment_type=employment_type)
            if is_active:
                employees = employees.filter(is_active=bool(int(is_active)))
    else:
        form = EmployeeReportFilterForm()
    
    # Statistics
    total_employees = employees.count()
    by_department = employees.values('department__name_ar').annotate(count=Count('id'))
    by_employment_type = employees.values('employment_type').annotate(count=Count('id'))
    
    context = {
        'form': form,
        'employees': employees,
        'total_employees': total_employees,
        'by_department': by_department,
        'by_employment_type': by_employment_type,
    }
    
    return render(request, 'reports/employee_summary_report.html', context)


@login_required
def attendance_summary_report(request):
    """
    Attendance summary report view
    عرض تقرير ملخص الحضور
    """
    # Default to current month
    today = timezone.now().date()
    start_date = today.replace(day=1)
    end_date = today
    
    if request.method == 'GET':
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date', start_date)
            end_date = form.cleaned_data.get('end_date', end_date)
    else:
        form = ReportFilterForm(initial={'start_date': start_date, 'end_date': end_date})
    
    # Get attendance data
    attendances = Attendance.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Statistics
    total_records = attendances.count()
    present_count = attendances.filter(status__in=['present', 'late']).count()
    late_count = attendances.filter(status='late').count()
    absent_count = attendances.filter(status='absent').count()
    
    # By employee
    by_employee = attendances.values(
        'employee__full_name_ar'
    ).annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status__in=['present', 'late'])),
        late=Count('id', filter=Q(status='late')),
        absent=Count('id', filter=Q(status='absent'))
    )
    
    context = {
        'form': form,
        'start_date': start_date,
        'end_date': end_date,
        'total_records': total_records,
        'present_count': present_count,
        'late_count': late_count,
        'absent_count': absent_count,
        'by_employee': by_employee,
    }
    
    return render(request, 'reports/attendance_summary_report.html', context)


@login_required
def attendance_monthly_report(request):
    """
    Monthly attendance report view
    عرض تقرير الحضور الشهري
    """
    # Default to current month
    today = timezone.now().date()
    start_date = today.replace(day=1)
    
    if request.method == 'GET':
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date', start_date)
    else:
        form = ReportFilterForm(initial={'start_date': start_date})
    
    # Calculate end date (last day of month)
    if start_date.month == 12:
        end_date = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
    
    # Get attendance data
    attendances = Attendance.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).select_related('employee')
    
    # Group by employee
    employees = Employee.objects.filter(is_active=True)
    employee_data = []
    
    for employee in employees:
        emp_attendances = attendances.filter(employee=employee)
        employee_data.append({
            'employee': employee,
            'total_days': emp_attendances.count(),
            'present': emp_attendances.filter(status__in=['present', 'late']).count(),
            'late': emp_attendances.filter(status='late').count(),
            'absent': emp_attendances.filter(status='absent').count(),
        })
    
    context = {
        'form': form,
        'start_date': start_date,
        'end_date': end_date,
        'employee_data': employee_data,
    }
    
    return render(request, 'reports/attendance_monthly_report.html', context)


@login_required
def leave_summary_report(request):
    """
    Leave summary report view
    عرض تقرير ملخص الإجازات
    """
    # Default to current year
    today = timezone.now().date()
    start_date = today.replace(month=1, day=1)
    end_date = today
    
    if request.method == 'GET':
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date', start_date)
            end_date = form.cleaned_data.get('end_date', end_date)
    else:
        form = ReportFilterForm(initial={'start_date': start_date, 'end_date': end_date})
    
    # Get leave data
    leaves = LeaveRequest.objects.filter(
        start_date__gte=start_date,
        end_date__lte=end_date
    )
    
    # Statistics
    total_requests = leaves.count()
    approved = leaves.filter(status='approved').count()
    pending = leaves.filter(status='pending').count()
    rejected = leaves.filter(status='rejected').count()
    
    # By leave type
    by_type = leaves.values('leave_type').annotate(count=Count('id'))
    
    # By employee
    by_employee = leaves.values(
        'employee__full_name_ar'
    ).annotate(
        total=Count('id'),
        total_days=Sum('days')
    )
    
    context = {
        'form': form,
        'start_date': start_date,
        'end_date': end_date,
        'total_requests': total_requests,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'by_type': by_type,
        'by_employee': by_employee,
    }
    
    return render(request, 'reports/leave_summary_report.html', context)


@login_required
def payroll_summary_report(request):
    """
    Payroll summary report view
    عرض تقرير ملخص الرواتب
    """
    payrolls = Payroll.objects.all().order_by('-year', '-month')
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        payrolls = payrolls.filter(year=year)
    
    # Get payslip statistics
    payroll_data = []
    for payroll in payrolls:
        payslips = Payslip.objects.filter(payroll=payroll)
        payroll_data.append({
            'payroll': payroll,
            'total_employees': payslips.count(),
            'total_basic_salary': payslips.aggregate(Sum('basic_salary'))['basic_salary__sum'] or 0,
            'total_net_salary': payslips.aggregate(Sum('net_salary'))['net_salary__sum'] or 0,
        })
    
    context = {
        'payroll_data': payroll_data,
    }
    
    return render(request, 'reports/payroll_summary_report.html', context)

