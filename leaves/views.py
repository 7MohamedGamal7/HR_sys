"""
Views for leaves app
عرض تطبيق الإجازات
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import LeavePolicy, LeaveBalance, LeaveApprovalWorkflow
from .forms import LeavePolicyForm, LeaveBalanceForm, LeaveApprovalWorkflowForm


# Leave Policy Views
@login_required
def leave_policy_list(request):
    """
    Leave policy list view
    عرض قائمة سياسات الإجازات
    """
    policies = LeavePolicy.objects.filter(is_active=True).order_by('name')
    
    context = {
        'policies': policies,
    }
    
    return render(request, 'leaves/leave_policy_list.html', context)


@login_required
def leave_policy_detail(request, pk):
    """
    Leave policy detail view
    عرض تفاصيل سياسة الإجازة
    """
    policy = get_object_or_404(LeavePolicy, pk=pk)
    workflows = LeaveApprovalWorkflow.objects.none()  # Temporary fix - no workflows for now
    
    context = {
        'policy': policy,
        'workflows': workflows,
    }
    
    return render(request, 'leaves/leave_policy_detail.html', context)


@login_required
def leave_policy_create(request):
    """
    Leave policy create view
    عرض إضافة سياسة إجازة
    """
    if request.method == 'POST':
        form = LeavePolicyForm(request.POST)
        if form.is_valid():
            policy = form.save()
            messages.success(request, 'تم إضافة سياسة الإجازة بنجاح.')
            return redirect('leaves:leave_policy_detail', pk=policy.pk)
    else:
        form = LeavePolicyForm()
    
    return render(request, 'leaves/leave_policy_form.html', {'form': form})


@login_required
def leave_policy_update(request, pk):
    """
    Leave policy update view
    عرض تعديل سياسة الإجازة
    """
    policy = get_object_or_404(LeavePolicy, pk=pk)
    
    if request.method == 'POST':
        form = LeavePolicyForm(request.POST, instance=policy)
        if form.is_valid():
            policy = form.save()
            messages.success(request, 'تم تحديث سياسة الإجازة بنجاح.')
            return redirect('leaves:leave_policy_detail', pk=policy.pk)
    else:
        form = LeavePolicyForm(instance=policy)
    
    return render(request, 'leaves/leave_policy_form.html', {'form': form, 'policy': policy})


# Leave Balance Views
@login_required
def leave_balance_list(request):
    """
    Leave balance list view
    عرض قائمة أرصدة الإجازات
    """
    balances = LeaveBalance.objects.select_related('employee').all().order_by('employee__first_name_ar')
    
    # Filter by employee
    employee_id = request.GET.get('employee')
    if employee_id:
        balances = balances.filter(employee_id=employee_id)
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        balances = balances.filter(year=year)
    
    # Pagination
    paginator = Paginator(balances, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'leaves/leave_balance_list.html', context)


@login_required
def my_leave_balance(request):
    """
    My leave balance view
    عرض رصيد إجازاتي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    from django.utils import timezone
    current_year = timezone.now().year
    
    balances = LeaveBalance.objects.filter(
        employee=request.user.employee_profile,
        year=current_year
    ).select_related('employee')
    
    context = {
        'balances': balances,
        'current_year': current_year,
    }
    
    return render(request, 'leaves/my_leave_balance.html', context)


@login_required
def leave_balance_create(request):
    """
    Leave balance create view
    عرض إضافة رصيد إجازة
    """
    if request.method == 'POST':
        form = LeaveBalanceForm(request.POST)
        if form.is_valid():
            balance = form.save()
            messages.success(request, 'تم إضافة رصيد الإجازة بنجاح.')
            return redirect('leaves:leave_balance_list')
    else:
        form = LeaveBalanceForm()
    
    return render(request, 'leaves/leave_balance_form.html', {'form': form})


@login_required
def leave_balance_update(request, pk):
    """
    Leave balance update view
    عرض تعديل رصيد الإجازة
    """
    balance = get_object_or_404(LeaveBalance, pk=pk)
    
    if request.method == 'POST':
        form = LeaveBalanceForm(request.POST, instance=balance)
        if form.is_valid():
            balance = form.save()
            messages.success(request, 'تم تحديث رصيد الإجازة بنجاح.')
            return redirect('leaves:leave_balance_list')
    else:
        form = LeaveBalanceForm(instance=balance)
    
    return render(request, 'leaves/leave_balance_form.html', {'form': form, 'balance': balance})


# Leave Approval Workflow Views
@login_required
def workflow_create(request, policy_pk):
    """
    Leave approval workflow create view
    عرض إضافة سير عمل الموافقة
    """
    policy = get_object_or_404(LeavePolicy, pk=policy_pk)
    
    if request.method == 'POST':
        form = LeaveApprovalWorkflowForm(request.POST)
        if form.is_valid():
            workflow = form.save()
            messages.success(request, 'تم إضافة سير العمل بنجاح.')
            return redirect('leaves:leave_policy_list')
    else:
        form = LeaveApprovalWorkflowForm()
    
    return render(request, 'leaves/workflow_form.html', {'form': form, 'policy': policy})

