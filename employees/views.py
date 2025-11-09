"""
Views for employees app
عرض تطبيق الموظفين
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee, EmployeeDocument, EmployeeContract, EmergencyContact, EmployeeEducation, EmployeeExperience
from .forms import (
    EmployeeForm, EmployeeDocumentForm, EmployeeContractForm,
    EmergencyContactForm, EmployeeEducationForm, EmployeeExperienceForm
)


@login_required
def employee_list(request):
    """
    Employee list view
    عرض قائمة الموظفين
    """
    employees = Employee.objects.select_related('department', 'position', 'branch').filter(is_active=True)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(employee_code__icontains=search_query) |
            Q(full_name_ar__icontains=search_query) |
            Q(full_name_en__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filter by department
    department_id = request.GET.get('department')
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    # Filter by employment type
    employment_type = request.GET.get('employment_type')
    if employment_type:
        employees = employees.filter(employment_type=employment_type)
    
    # Pagination
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """
    Employee detail view
    عرض تفاصيل الموظف
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    # Get related data
    documents = EmployeeDocument.objects.filter(employee=employee)
    contracts = EmployeeContract.objects.filter(employee=employee).order_by('-start_date')
    emergency_contacts = EmergencyContact.objects.filter(employee=employee)
    education = EmployeeEducation.objects.filter(employee=employee).order_by('-graduation_year')
    experience = EmployeeExperience.objects.filter(employee=employee).order_by('-start_date')
    
    context = {
        'employee': employee,
        'documents': documents,
        'contracts': contracts,
        'emergency_contacts': emergency_contacts,
        'education': education,
        'experience': experience,
    }
    
    return render(request, 'employees/employee_detail.html', context)


@login_required
def employee_create(request):
    """
    Employee create view
    عرض إضافة موظف
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'تم إضافة الموظف {employee.full_name_ar} بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'إضافة'})


@login_required
def employee_update(request, pk):
    """
    Employee update view
    عرض تعديل الموظف
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'تم تحديث بيانات الموظف {employee.full_name_ar} بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'تعديل', 'employee': employee})


@login_required
def employee_delete(request, pk):
    """
    Employee delete view (soft delete)
    عرض حذف الموظف
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
        messages.success(request, f'تم حذف الموظف {employee.full_name_ar} بنجاح.')
        return redirect('employees:employee_list')
    
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


# Employee Documents Views
@login_required
def employee_document_create(request, employee_pk):
    """
    Employee document create view
    عرض إضافة مستند موظف
    """
    employee = get_object_or_404(Employee, pk=employee_pk)
    
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee
            document.save()
            messages.success(request, 'تم إضافة المستند بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeDocumentForm()
    
    return render(request, 'employees/document_form.html', {'form': form, 'employee': employee})


@login_required
def employee_document_delete(request, pk):
    """
    Employee document delete view
    عرض حذف مستند موظف
    """
    document = get_object_or_404(EmployeeDocument, pk=pk)
    employee = document.employee
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'تم حذف المستند بنجاح.')
        return redirect('employees:employee_detail', pk=employee.pk)
    
    return render(request, 'employees/document_confirm_delete.html', {'document': document})


# Employee Contract Views
@login_required
def employee_contract_create(request, employee_pk):
    """
    Employee contract create view
    عرض إضافة عقد موظف
    """
    employee = get_object_or_404(Employee, pk=employee_pk)
    
    if request.method == 'POST':
        form = EmployeeContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.employee = employee
            contract.save()
            messages.success(request, 'تم إضافة العقد بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeContractForm()
    
    return render(request, 'employees/contract_form.html', {'form': form, 'employee': employee})


@login_required
def employee_contract_update(request, pk):
    """
    Employee contract update view
    عرض تعديل عقد موظف
    """
    contract = get_object_or_404(EmployeeContract, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث العقد بنجاح.')
            return redirect('employees:employee_detail', pk=contract.employee.pk)
    else:
        form = EmployeeContractForm(instance=contract)
    
    return render(request, 'employees/contract_form.html', {'form': form, 'contract': contract})


# Emergency Contact Views
@login_required
def emergency_contact_create(request, employee_pk):
    """
    Emergency contact create view
    عرض إضافة جهة اتصال طوارئ
    """
    employee = get_object_or_404(Employee, pk=employee_pk)
    
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.employee = employee
            contact.save()
            messages.success(request, 'تم إضافة جهة الاتصال بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmergencyContactForm()
    
    return render(request, 'employees/emergency_contact_form.html', {'form': form, 'employee': employee})


# Education Views
@login_required
def employee_education_create(request, employee_pk):
    """
    Employee education create view
    عرض إضافة مؤهل تعليمي
    """
    employee = get_object_or_404(Employee, pk=employee_pk)
    
    if request.method == 'POST':
        form = EmployeeEducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.employee = employee
            education.save()
            messages.success(request, 'تم إضافة المؤهل التعليمي بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeEducationForm()
    
    return render(request, 'employees/education_form.html', {'form': form, 'employee': employee})


# Experience Views
@login_required
def employee_experience_create(request, employee_pk):
    """
    Employee experience create view
    عرض إضافة خبرة عملية
    """
    employee = get_object_or_404(Employee, pk=employee_pk)
    
    if request.method == 'POST':
        form = EmployeeExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.employee = employee
            experience.save()
            messages.success(request, 'تم إضافة الخبرة العملية بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeExperienceForm()
    
    return render(request, 'employees/experience_form.html', {'form': form, 'employee': employee})

