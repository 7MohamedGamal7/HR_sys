"""
Views for employees app
عرض تطبيق الموظفين
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from crispy_forms.helper import FormHelper
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from organization.models import Department
from .models import (
    Employee, EmployeeDocument, EmployeeContract, EmergencyContact,
    EmployeeEducation, EmployeeExperience, EmployeeInsurance, EmployeeCustody
)
from .forms import (
    EmployeeForm, EmployeeDocumentForm, EmployeeContractForm,
    EmergencyContactForm, EmployeeEducationForm, EmployeeExperienceForm,
    EmployeeInsuranceForm, EmployeeCustodyForm
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
            Q(emp_code__icontains=search_query) |
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
        'departments': Department.objects.all(),
    }
    
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """
    Employee detail view
    عرض تفاصيل الموظف
    """
    employee = get_object_or_404(Employee, pk=pk)

    # Get related data - using related_name from models
    documents = employee.documents.all()
    contracts = employee.contracts.all().order_by('-start_date')
    emergency_contacts = employee.emergency_contacts.all()
    experience = employee.experience.all().order_by('-start_date')
    insurances = employee.insurances.all()
    health_insurances = employee.insurances.filter(insurance_type='health')
    social_insurances = employee.insurances.filter(insurance_type='social')
    custodies = employee.custodies.all()
    qualifications = employee.qualifications.all().order_by('-graduation_year')
    education = employee.education.all().order_by('-graduation_year')
    
    from datetime import date
    today = date.today()

    context = {
        'employee': employee,
        'documents': documents,
        'contracts': contracts,
        'emergency_contacts': emergency_contacts,
        'experience': experience,
        'insurances': insurances,
        'health_insurances': health_insurances,
        'social_insurances': social_insurances,
        'custodies': custodies,
        'qualifications': qualifications,
        'education': education,
        'today': today,
    }

    return render(request, 'employees/employee_detail_comprehensive.html', context)


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
            messages.success(request, f'تم إضافة الموظف {employee.get_full_name_ar()} بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_form_comprehensive.html', {'form': form, 'action': 'إضافة'})


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
            messages.success(request, f'تم تحديث بيانات الموظف {employee.get_full_name_ar()} بنجاح.')
            return redirect('employees:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)

    documents = employee.documents.all()
    contracts = employee.contracts.all().order_by('-start_date')
    insurances = employee.insurances.all()
    custodies = employee.custodies.all()
    education = employee.education.all().order_by('-graduation_year')
    experience = employee.experience.all().order_by('-start_date')

    document_form = EmployeeDocumentForm()
    contract_form = EmployeeContractForm()
    insurance_form = EmployeeInsuranceForm()
    custody_form = EmployeeCustodyForm()
    education_form = EmployeeEducationForm()
    experience_form = EmployeeExperienceForm()

    if not hasattr(insurance_form, 'helper'):
        insurance_form.helper = FormHelper()
        insurance_form.helper.form_method = 'post'
    if not hasattr(custody_form, 'helper'):
        custody_form.helper = FormHelper()
        custody_form.helper.form_method = 'post'
    if not hasattr(experience_form, 'helper'):
        experience_form.helper = FormHelper()
        experience_form.helper.form_method = 'post'

    document_form.helper.form_action = reverse('employees:document_create', args=[employee.pk])
    contract_form.helper.form_action = reverse('employees:contract_create', args=[employee.pk])
    insurance_form.helper.form_action = reverse('employees:insurance_create', args=[employee.pk])
    custody_form.helper.form_action = reverse('employees:custody_create', args=[employee.pk])
    education_form.helper.form_action = reverse('employees:education_create', args=[employee.pk])
    experience_form.helper.form_action = reverse('employees:experience_create', args=[employee.pk])

    context = {
        'form': form,
        'action': 'تعديل',
        'employee': employee,
        'documents': documents,
        'contracts': contracts,
        'insurances': insurances,
        'custodies': custodies,
        'education': education,
        'experience': experience,
        'document_form': document_form,
        'contract_form': contract_form,
        'insurance_form': insurance_form,
        'custody_form': custody_form,
        'education_form': education_form,
        'experience_form': experience_form,
    }

    return render(request, 'employees/employee_form_comprehensive.html', context)


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


@login_required
def employee_insurance_create(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeInsuranceForm(request.POST)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.employee = employee
            insurance.save()
            messages.success(request, 'تم إضافة التأمين بنجاح.')
            return redirect('employees:employee_update', pk=employee.pk)
    return redirect('employees:employee_update', pk=employee.pk)


@login_required
def employee_custody_create(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeCustodyForm(request.POST)
        if form.is_valid():
            custody = form.save(commit=False)
            custody.employee = employee
            custody.save()
            messages.success(request, 'تم إضافة العهدة بنجاح.')
            return redirect('employees:employee_update', pk=employee.pk)
    return redirect('employees:employee_update', pk=employee.pk)


@login_required
def employee_photo_upload(request, pk):
    """
    Upload employee photo view
    رفع صورة الموظف
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST' and request.FILES.get('photo'):
        employee.photo = request.FILES['photo']
        employee.save()
        messages.success(request, 'تم تحديث صورة الموظف بنجاح.')
        return redirect('employees:employee_detail', pk=pk)


@login_required
def employee_inline_update(request, pk):
    """
    Handle inline updates from employee detail tabs
    معالجة التحديثات المضمنة من تبويبات تفاصيل الموظف
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        employee = get_object_or_404(Employee, pk=pk)
        data = json.loads(request.body) if request.body else {}
        
        # Process different types of updates based on the tab
        updated_items = []
        errors = []
        
        # Process insurance updates
        if 'insurance' in data:
            for item_data in data['insurance']:
                try:
                    if 'id' in item_data:
                        # Update existing insurance
                        insurance = EmployeeInsurance.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeInsuranceForm(item_data, instance=insurance)
                    else:
                        # Create new insurance
                        form = EmployeeInsuranceForm(item_data)
                    
                    if form.is_valid():
                        insurance = form.save(commit=False)
                        insurance.employee = employee
                        insurance.save()
                        updated_items.append({'type': 'insurance', 'id': insurance.id})
                    else:
                        errors.append(f"Insurance error: {form.errors}")
                except EmployeeInsurance.DoesNotExist:
                    errors.append("Insurance not found")
        
        # Process contract updates
        if 'contracts' in data:
            for item_data in data['contracts']:
                try:
                    if 'id' in item_data:
                        contract = EmployeeContract.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeContractForm(item_data, instance=contract)
                    else:
                        form = EmployeeContractForm(item_data)
                    
                    if form.is_valid():
                        contract = form.save(commit=False)
                        contract.employee = employee
                        contract.save()
                        updated_items.append({'type': 'contract', 'id': contract.id})
                    else:
                        errors.append(f"Contract error: {form.errors}")
                except EmployeeContract.DoesNotExist:
                    errors.append("Contract not found")
        
        # Process custody updates
        if 'custody' in data:
            for item_data in data['custody']:
                try:
                    if 'id' in item_data:
                        custody = EmployeeCustody.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeCustodyForm(item_data, instance=custody)
                    else:
                        form = EmployeeCustodyForm(item_data)
                    
                    if form.is_valid():
                        custody = form.save(commit=False)
                        custody.employee = employee
                        custody.save()
                        updated_items.append({'type': 'custody', 'id': custody.id})
                    else:
                        errors.append(f"Custody error: {form.errors}")
                except EmployeeCustody.DoesNotExist:
                    errors.append("Custody not found")
        
        # Process document updates
        if 'documents' in data:
            for item_data in data['documents']:
                try:
                    if 'id' in item_data:
                        document = EmployeeDocument.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeDocumentForm(item_data, request.FILES, instance=document)
                    else:
                        form = EmployeeDocumentForm(item_data, request.FILES)
                    
                    if form.is_valid():
                        document = form.save(commit=False)
                        document.employee = employee
                        document.save()
                        updated_items.append({'type': 'document', 'id': document.id})
                    else:
                        errors.append(f"Document error: {form.errors}")
                except EmployeeDocument.DoesNotExist:
                    errors.append("Document not found")
        
        # Process education updates
        if 'education' in data:
            for item_data in data['education']:
                try:
                    if 'id' in item_data:
                        education = EmployeeEducation.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeEducationForm(item_data, instance=education)
                    else:
                        form = EmployeeEducationForm(item_data)
                    
                    if form.is_valid():
                        education = form.save(commit=False)
                        education.employee = employee
                        education.save()
                        updated_items.append({'type': 'education', 'id': education.id})
                    else:
                        errors.append(f"Education error: {form.errors}")
                except EmployeeEducation.DoesNotExist:
                    errors.append("Education not found")
        
        # Process experience updates
        if 'experience' in data:
            for item_data in data['experience']:
                try:
                    if 'id' in item_data:
                        experience = EmployeeExperience.objects.get(id=item_data['id'], employee=employee)
                        form = EmployeeExperienceForm(item_data, instance=experience)
                    else:
                        form = EmployeeExperienceForm(item_data)
                    
                    if form.is_valid():
                        experience = form.save(commit=False)
                        experience.employee = employee
                        experience.save()
                        updated_items.append({'type': 'experience', 'id': experience.id})
                    else:
                        errors.append(f"Experience error: {form.errors}")
                except EmployeeExperience.DoesNotExist:
                    errors.append("Experience not found")
        
        if errors and not updated_items:
            return JsonResponse({'success': False, 'error': '; '.join(errors)})
        
        return JsonResponse({
            'success': True, 
            'updated_items': updated_items,
            'errors': errors if errors else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def employee_item_get(request, item_type, item_id):
    """
    Get individual item data for editing
    الحصول على بيانات عنصر فردي للتعديل
    """
    try:
        # Map item types to models and forms
        type_mapping = {
            'insurance': {'model': EmployeeInsurance, 'form': EmployeeInsuranceForm},
            'contract': {'model': EmployeeContract, 'form': EmployeeContractForm},
            'custody': {'model': EmployeeCustody, 'form': EmployeeCustodyForm},
            'document': {'model': EmployeeDocument, 'form': EmployeeDocumentForm},
            'education': {'model': EmployeeEducation, 'form': EmployeeEducationForm},
            'experience': {'model': EmployeeExperience, 'form': EmployeeExperienceForm},
        }
        
        if item_type not in type_mapping:
            return JsonResponse({'success': False, 'error': 'Invalid item type'})
        
        mapping = type_mapping[item_type]
        item = get_object_or_404(mapping['model'], pk=item_id)
        
        # Serialize item data
        if item_type == 'insurance':
            data = {
                'id': item.id,
                'insurance_type': item.insurance_type,
                'insurance_number': item.insurance_number,
                'insurance_company': item.insurance_company,
                'start_date': item.start_date.isoformat() if item.start_date else '',
                'end_date': item.end_date.isoformat() if item.end_date else '',
                'notes': item.notes or '',
            }
        elif item_type == 'contract':
            data = {
                'id': item.id,
                'contract_number': item.contract_number,
                'contract_type': item.contract_type,
                'start_date': item.start_date.isoformat() if item.start_date else '',
                'end_date': item.end_date.isoformat() if item.end_date else '',
                'basic_salary': str(item.basic_salary) if item.basic_salary else '',
                'housing_allowance': str(item.housing_allowance) if item.housing_allowance else '',
                'transportation_allowance': str(item.transportation_allowance) if item.transportation_allowance else '',
                'other_allowances': str(item.other_allowances) if item.other_allowances else '',
                'notes': item.notes or '',
            }
        elif item_type == 'custody':
            data = {
                'id': item.id,
                'custody_type': item.custody_type,
                'item_name': item.item_name,
                'serial_number': item.serial_number,
                'value': str(item.value) if item.value else '',
                'issue_date': item.issue_date.isoformat() if item.issue_date else '',
                'status': item.status,
                'notes': item.notes or '',
            }
        elif item_type == 'document':
            data = {
                'id': item.id,
                'document_type': item.document_type,
                'document_title': item.document_title,
                'issuing_authority': item.issuing_authority or '',
                'issue_date': item.issue_date.isoformat() if item.issue_date else '',
                'expiry_date': item.expiry_date.isoformat() if item.expiry_date else '',
                'notes': item.notes or '',
            }
        elif item_type == 'education':
            data = {
                'id': item.id,
                'degree_level': item.degree_level,
                'major': item.major,
                'institution': item.institution,
                'graduation_year': item.graduation_year,
                'gpa': str(item.gpa) if item.gpa else '',
                'notes': item.notes or '',
            }
        elif item_type == 'experience':
            data = {
                'id': item.id,
                'company_name': item.company_name,
                'position': item.position,
                'industry': item.industry,
                'start_date': item.start_date.isoformat() if item.start_date else '',
                'end_date': item.end_date.isoformat() if item.end_date else '',
                'is_current': item.is_current,
                'salary': str(item.salary) if item.salary else '',
                'responsibilities': item.responsibilities or '',
                'achievements': item.achievements or '',
            }
        
        return JsonResponse({'success': True, 'item': data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def employee_item_delete(request, item_type, item_id):
    """
    Delete individual item
    حذف عنصر فردي
    """
    try:
        # Map item types to models
        type_mapping = {
            'insurance': EmployeeInsurance,
            'contract': EmployeeContract,
            'custody': EmployeeCustody,
            'document': EmployeeDocument,
            'education': EmployeeEducation,
            'experience': EmployeeExperience,
        }
        
        if item_type not in type_mapping:
            return JsonResponse({'success': False, 'error': 'Invalid item type'})
        
        model = type_mapping[item_type]
        item = get_object_or_404(model, pk=item_id)
        item.delete()
        
        return JsonResponse({'success': True, 'message': 'Item deleted successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

