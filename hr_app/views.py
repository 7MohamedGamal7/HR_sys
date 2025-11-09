from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .forms import CustomAuthenticationForm, EmployeeForm, LeaveForm, SettingsForm
from .models import (
    TblEmployees, TblAttendance, TblLates, TblLeaves, 
    TblLoans, TblLogs, TblOvertime, TblPayslips, TblSettings
)
from datetime import datetime, date
import json


# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'hr_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# Dashboard View
@login_required
def dashboard_view(request):
    # Get statistics
    total_employees = TblEmployees.objects.filter(is_active=True).count()
    present_today = TblAttendance.objects.filter(
        attendance_date=date.today()
    ).count()
    leaves_today = TblLeaves.objects.filter(
        start_date__lte=date.today(),
        end_date__gte=date.today(),
        status='Approved'
    ).count()
    pending_loans = TblLoans.objects.filter(status='Pending').count()
    
    # Get recent activities
    recent_logs = TblLogs.objects.all().order_by('-performed_at')[:5]
    
    # Get upcoming leaves
    upcoming_leaves = TblLeaves.objects.filter(
        start_date__gte=date.today(),
        status='Approved'
    ).order_by('start_date')[:5]
    
    # Get recent lates
    recent_lates = TblLates.objects.all().order_by('-late_date')[:5]
    
    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'leaves_today': leaves_today,
        'pending_loans': pending_loans,
        'recent_logs': recent_logs,
        'upcoming_leaves': upcoming_leaves,
        'recent_lates': recent_lates,
    }
    
    return render(request, 'hr_app/dashboard.html', context)


# Employee Management Views
@login_required
def employees_view(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Filter employees
    if search_query:
        employees = TblEmployees.objects.filter(
            Q(emp_fullname__icontains=search_query) |
            Q(emp_code__icontains=search_query) |
            Q(job_title__icontains=search_query) |
            Q(department__icontains=search_query)
        )
    else:
        employees = TblEmployees.objects.all()
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        employees = employees.filter(is_active=True)
    elif status_filter == 'inactive':
        employees = employees.filter(is_active=False)
    
    # Paginate employees
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employees': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'hr_app/employees.html', context)


@login_required
def employee_detail_view(request, emp_id):
    employee = get_object_or_404(TblEmployees, emp_id=emp_id)
    
    # Get employee leaves
    employee_leaves = TblLeaves.objects.filter(emp=employee).order_by('-start_date')[:5]
    
    # Get employee payslips
    employee_payslips = TblPayslips.objects.filter(emp=employee).order_by('-period_end')[:5]
    
    context = {
        'employee': employee,
        'employee_leaves': employee_leaves,
        'employee_payslips': employee_payslips,
    }
    
    return render(request, 'hr_app/employee_detail.html', context)


@login_required
def add_employee_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to database yet
            employee = form.save(commit=False)
            # Calculate salary_total manually
            basic = employee.salary_basic or 0
            housing = employee.salary_housing or 0
            transport = employee.salary_transport or 0
            other = employee.salary_other or 0
            employee.salary_total = basic + housing + transport + other
            # Now save to database
            employee.save()
            messages.success(request, f'Employee {employee.emp_fullname} added successfully!')
            return redirect('employees')
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
        'title': 'Add Employee',
    }
    
    return render(request, 'hr_app/employee_form.html', context)


@login_required
def edit_employee_view(request, emp_id):
    employee = get_object_or_404(TblEmployees, emp_id=emp_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            # Save the form but don't commit to database yet
            employee = form.save(commit=False)
            # Calculate salary_total manually
            basic = employee.salary_basic or 0
            housing = employee.salary_housing or 0
            transport = employee.salary_transport or 0
            other = employee.salary_other or 0
            employee.salary_total = basic + housing + transport + other
            # Now save to database
            employee.save()
            messages.success(request, f'Employee {employee.emp_fullname} updated successfully!')
            return redirect('view_employee', emp_id=employee.emp_id)
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
        'title': 'Edit Employee',
    }
    
    return render(request, 'hr_app/employee_form.html', context)


@login_required
def delete_employee_view(request, emp_id):
    employee = get_object_or_404(TblEmployees, emp_id=emp_id)
    
    if request.method == 'POST':
        employee_name = employee.emp_fullname
        employee.delete()
        messages.success(request, f'Employee {employee_name} deleted successfully!')
        return redirect('employees')
    
    context = {
        'employee': employee,
    }
    
    return render(request, 'hr_app/employee_confirm_delete.html', context)


# Attendance Management Views
@login_required
def attendance_view(request):
    # Get filters
    selected_date = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
    search_query = request.GET.get('search', '')
    
    # Filter attendance records
    attendance_records = TblAttendance.objects.all()
    
    if selected_date:
        attendance_records = attendance_records.filter(attendance_date=selected_date)
    
    if search_query:
        attendance_records = attendance_records.filter(
            Q(emp__emp_fullname__icontains=search_query) |
            Q(emp__emp_code__icontains=search_query)
        )
    
    # Paginate records
    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'attendance_records': page_obj,
        'selected_date': selected_date,
        'search_query': search_query,
    }
    
    return render(request, 'hr_app/attendance.html', context)


# Leave Management Views
@login_required
def leaves_view(request):
    # Get filters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Filter leaves
    leaves = TblLeaves.objects.all()
    
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    
    if search_query:
        leaves = leaves.filter(
            Q(emp__emp_fullname__icontains=search_query) |
            Q(leave_type__icontains=search_query)
        )
    
    # Paginate leaves
    paginator = Paginator(leaves, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'leaves': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'hr_app/leaves.html', context)


@login_required
def apply_leave_view(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save()
            messages.success(request, 'Leave application submitted successfully!')
            return redirect('leaves')
    else:
        form = LeaveForm()
    
    context = {
        'form': form,
        'title': 'Apply for Leave',
    }
    
    return render(request, 'hr_app/leave_form.html', context)


@login_required
def approve_leave_view(request, leave_id):
    leave = get_object_or_404(TblLeaves, leave_id=leave_id)
    leave.status = 'Approved'
    leave.approved_by = request.user.username
    leave.save()
    messages.success(request, f'Leave for {leave.emp.emp_fullname} approved successfully!')
    return redirect('leaves')


@login_required
def reject_leave_view(request, leave_id):
    leave = get_object_or_404(TblLeaves, leave_id=leave_id)
    leave.status = 'Rejected'
    leave.approved_by = request.user.username
    leave.save()
    messages.success(request, f'Leave for {leave.emp.emp_fullname} rejected successfully!')
    return redirect('leaves')


# Payroll Management Views
@login_required
def payroll_view(request):
    # Get filters
    selected_month = request.GET.get('month', date.today().strftime('%Y-%m'))
    search_query = request.GET.get('search', '')
    
    # Filter payslips
    payslips = TblPayslips.objects.all()
    
    if selected_month:
        year, month = selected_month.split('-')
        payslips = payslips.filter(
            period_end__year=year,
            period_end__month=month
        )
    
    if search_query:
        payslips = payslips.filter(
            Q(emp__emp_fullname__icontains=search_query) |
            Q(emp__emp_code__icontains=search_query)
        )
    
    # Paginate payslips
    paginator = Paginator(payslips, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'payslips': page_obj,
        'selected_month': selected_month,
        'search_query': search_query,
    }
    
    return render(request, 'hr_app/payroll.html', context)


@login_required
def edit_payslip_view(request, payslip_id):
    payslip = get_object_or_404(TblPayslips, payslip_id=payslip_id)
    
    if request.method == 'POST':
        # Handle payslip editing
        messages.success(request, f'Payslip for {payslip.emp.emp_fullname} updated successfully!')
        return redirect('payroll')
    
    context = {
        'payslip': payslip,
    }
    
    return render(request, 'hr_app/payslip_form.html', context)


@login_required
def delete_payslip_view(request, payslip_id):
    payslip = get_object_or_404(TblPayslips, payslip_id=payslip_id)
    
    if request.method == 'POST':
        payslip_name = f"Payslip for {payslip.emp.emp_fullname}"
        payslip.delete()
        messages.success(request, f'{payslip_name} deleted successfully!')
        return redirect('payroll')
    
    context = {
        'payslip': payslip,
    }
    
    return render(request, 'hr_app/payslip_confirm_delete.html', context)


# Reports View
@login_required
def reports_view(request):
    # Get filters
    report_type = request.GET.get('type', 'attendance')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    department = request.GET.get('department', '')
    
    # Sample report data
    report_data = []
    if report_type == 'attendance':
        report_data = [
            {'employee': 'John Doe', 'department': 'IT', 'total_days': 22, 'present': 20, 'absent': 2, 'late': 3, 'avg_hours': 8.2},
            {'employee': 'Jane Smith', 'department': 'HR', 'total_days': 22, 'present': 22, 'absent': 0, 'late': 1, 'avg_hours': 8.5},
            # Add more sample data
        ]
    elif report_type == 'leave':
        report_data = [
            {'employee': 'John Doe', 'department': 'IT', 'total_leaves': 5, 'approved': 4, 'pending': 1, 'rejected': 0, 'total_days': 10},
            {'employee': 'Jane Smith', 'department': 'HR', 'total_leaves': 3, 'approved': 3, 'pending': 0, 'rejected': 0, 'total_days': 6},
            # Add more sample data
        ]
    elif report_type == 'payroll':
        report_data = [
            {'employee': 'John Doe', 'department': 'IT', 'gross_pay': 5000, 'deductions': 500, 'net_pay': 4500, 'total_loans': 1000},
            {'employee': 'Jane Smith', 'department': 'HR', 'gross_pay': 4500, 'deductions': 400, 'net_pay': 4100, 'total_loans': 0},
            # Add more sample data
        ]
    else:  # employee report
        report_data = [
            {'employee': 'John Doe', 'job_title': 'Software Engineer', 'department': 'IT', 'hire_date': '2020-01-15', 'status': True, 'salary': 5000},
            {'employee': 'Jane Smith', 'job_title': 'HR Manager', 'department': 'HR', 'hire_date': '2019-03-20', 'status': True, 'salary': 4500},
            # Add more sample data
        ]
    
    context = {
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
        'department': department,
        'report_data': report_data,
    }
    
    return render(request, 'hr_app/reports.html', context)


# Settings View
@login_required
def settings_view(request):
    # Get or create settings
    settings, created = TblSettings.objects.get_or_create(
        setting_id=1,
        defaults={
            'company_name': 'Acrylica Company',
            'workday_start': '09:00:00',
            'workday_end': '17:00:00',
            'lunch_break_minutes': 60,
            'late_threshold_min': 15,
            'overtime_rate': 1.5,
            'monthly_working_hours': 160,
            'salary_currency': 'USD',
        }
    )
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings)
    
    context = {
        'settings': settings,
        'form': form,
    }
    
    return render(request, 'hr_app/settings.html', context)