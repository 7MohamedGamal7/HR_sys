"""
Views for organization app
عرض تطبيق الهيكل التنظيمي
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Department, Position, Branch, WorkShift, Holiday
from .forms import DepartmentForm, PositionForm, BranchForm, WorkShiftForm, HolidayForm


# Department Views
@login_required
def department_list(request):
    """
    Department list view
    عرض قائمة الأقسام
    """
    departments = Department.objects.filter(is_active=True).order_by('dept_name_ar')

    context = {
        'departments': departments,
    }

    return render(request, 'organization/department_list.html', context)


@login_required
def department_detail(request, pk):
    """
    Department detail view
    عرض تفاصيل القسم
    """
    department = get_object_or_404(Department, pk=pk)
    
    # Get employees in this department
    employees = department.employees.filter(is_active=True)

    # Get sub-departments
    sub_departments = Department.objects.filter(parent_department=department, is_active=True)
    
    context = {
        'department': department,
        'employees': employees,
        'sub_departments': sub_departments,
    }
    
    return render(request, 'organization/department_detail.html', context)


@login_required
def department_create(request):
    """
    Department create view
    عرض إضافة قسم
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'تم إضافة القسم {department.dept_name_ar} بنجاح.')
            return redirect('organization:department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'organization/department_form.html', {'form': form, 'action': 'إضافة'})


@login_required
def department_update(request, pk):
    """
    Department update view
    عرض تعديل القسم
    """
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'تم تحديث القسم {department.dept_name_ar} بنجاح.')
            return redirect('organization:department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'organization/department_form.html', {'form': form, 'action': 'تعديل', 'department': department})


@login_required
def department_delete(request, pk):
    """
    Department delete view (soft delete)
    عرض حذف القسم
    """
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department.is_active = False
        department.save()
        messages.success(request, f'تم حذف القسم {department.dept_name_ar} بنجاح.')
        return redirect('organization:department_list')
    
    return render(request, 'organization/department_confirm_delete.html', {'department': department})


# Position Views
@login_required
def position_list(request):
    """
    Position list view
    عرض قائمة المناصب
    """
    positions = Position.objects.select_related('department').filter(is_active=True).order_by('position_name_ar')

    # Pagination
    paginator = Paginator(positions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'organization/position_list.html', context)


@login_required
def position_create(request):
    """
    Position create view
    عرض إضافة منصب
    """
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            messages.success(request, f'تم إضافة المنصب {position.position_name_ar} بنجاح.')
            return redirect('organization:position_list')
    else:
        form = PositionForm()
    
    return render(request, 'organization/position_form.html', {'form': form})


@login_required
def position_update(request, pk):
    """
    Position update view
    عرض تعديل المنصب
    """
    position = get_object_or_404(Position, pk=pk)
    
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save()
            messages.success(request, f'تم تحديث المنصب {position.position_name_ar} بنجاح.')
            return redirect('organization:position_list')
    else:
        form = PositionForm(instance=position)
    
    return render(request, 'organization/position_form.html', {'form': form, 'position': position})


# Branch Views
@login_required
def branch_list(request):
    """
    Branch list view
    عرض قائمة الفروع
    """
    branches = Branch.objects.filter(is_active=True).order_by('branch_name_ar')

    context = {
        'branches': branches,
    }

    return render(request, 'organization/branch_list.html', context)


@login_required
def branch_create(request):
    """
    Branch create view
    عرض إضافة فرع
    """
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()
            messages.success(request, f'تم إضافة الفرع {branch.branch_name_ar} بنجاح.')
            return redirect('organization:branch_list')
    else:
        form = BranchForm()
    
    return render(request, 'organization/branch_form.html', {'form': form})


@login_required
def branch_update(request, pk):
    """
    Branch update view
    عرض تعديل الفرع
    """
    branch = get_object_or_404(Branch, pk=pk)
    
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            branch = form.save()
            messages.success(request, f'تم تحديث الفرع {branch.branch_name_ar} بنجاح.')
            return redirect('organization:branch_list')
    else:
        form = BranchForm(instance=branch)
    
    return render(request, 'organization/branch_form.html', {'form': form, 'branch': branch})


# Work Shift Views
@login_required
def shift_list(request):
    """
    Work shift list view
    عرض قائمة الورديات
    """
    shifts = WorkShift.objects.filter(is_active=True).order_by('shift_name')
    
    context = {
        'shifts': shifts,
    }
    
    return render(request, 'organization/shift_list.html', context)


@login_required
def shift_create(request):
    """
    Work shift create view
    عرض إضافة وردية
    """
    if request.method == 'POST':
        form = WorkShiftForm(request.POST)
        if form.is_valid():
            shift = form.save()
            messages.success(request, f'تم إضافة الوردية {shift.shift_name} بنجاح.')
            return redirect('organization:shift_list')
    else:
        form = WorkShiftForm()
    
    return render(request, 'organization/shift_form.html', {'form': form})


@login_required
def shift_update(request, pk):
    """
    Work shift update view
    عرض تعديل الوردية
    """
    shift = get_object_or_404(WorkShift, pk=pk)
    
    if request.method == 'POST':
        form = WorkShiftForm(request.POST, instance=shift)
        if form.is_valid():
            shift = form.save()
            messages.success(request, f'تم تحديث الوردية {shift.shift_name} بنجاح.')
            return redirect('organization:shift_list')
    else:
        form = WorkShiftForm(instance=shift)
    
    return render(request, 'organization/shift_form.html', {'form': form, 'shift': shift})


# Holiday Views
@login_required
def holiday_list(request):
    """
    Holiday list view
    عرض قائمة العطلات
    """
    holidays = Holiday.objects.all().order_by('date')
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        holidays = holidays.filter(date__year=year)
    
    context = {
        'holidays': holidays,
    }
    
    return render(request, 'organization/holiday_list.html', context)


@login_required
def holiday_create(request):
    """
    Holiday create view
    عرض إضافة عطلة
    """
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save()
            messages.success(request, f'تم إضافة العطلة {holiday.name} بنجاح.')
            return redirect('organization:holiday_list')
    else:
        form = HolidayForm()
    
    return render(request, 'organization/holiday_form.html', {'form': form})


@login_required
def holiday_update(request, pk):
    """
    Holiday update view
    عرض تعديل العطلة
    """
    holiday = get_object_or_404(Holiday, pk=pk)
    
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            holiday = form.save()
            messages.success(request, f'تم تحديث العطلة {holiday.name} بنجاح.')
            return redirect('organization:holiday_list')
    else:
        form = HolidayForm(instance=holiday)
    
    return render(request, 'organization/holiday_form.html', {'form': form, 'holiday': holiday})


@login_required
def holiday_delete(request, pk):
    """
    Holiday delete view
    عرض حذف العطلة
    """
    holiday = get_object_or_404(Holiday, pk=pk)
    
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, f'تم حذف العطلة {holiday.name} بنجاح.')
        return redirect('organization:holiday_list')
    
    return render(request, 'organization/holiday_confirm_delete.html', {'holiday': holiday})

