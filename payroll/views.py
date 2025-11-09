"""
Views for payroll app
عرض تطبيق الرواتب
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Payroll, Payslip, Loan, Bonus
from .forms import PayrollForm, PayslipForm, LoanForm, BonusForm


# Payroll Views
@login_required
def payroll_list(request):
    """
    Payroll list view
    عرض قائمة كشوف الرواتب
    """
    payrolls = Payroll.objects.all().order_by('-year', '-month')
    
    # Pagination
    paginator = Paginator(payrolls, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'payroll/payroll_list.html', context)


@login_required
def payroll_detail(request, pk):
    """
    Payroll detail view
    عرض تفاصيل كشف الرواتب
    """
    payroll = get_object_or_404(Payroll, pk=pk)
    payslips = Payslip.objects.filter(payroll=payroll).select_related('employee')
    
    context = {
        'payroll': payroll,
        'payslips': payslips,
    }
    
    return render(request, 'payroll/payroll_detail.html', context)


@login_required
def payroll_create(request):
    """
    Payroll create view
    عرض إنشاء كشف رواتب
    """
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save()
            messages.success(request, 'تم إنشاء كشف الرواتب بنجاح.')
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollForm()
    
    return render(request, 'payroll/payroll_form.html', {'form': form})


# Payslip Views
@login_required
def payslip_list(request):
    """
    Payslip list view
    عرض قائمة قسائم الرواتب
    """
    payslips = Payslip.objects.select_related('employee', 'payroll').all().order_by('-payroll__year', '-payroll__month')
    
    # Pagination
    paginator = Paginator(payslips, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'payroll/payslip_list.html', context)


@login_required
def my_payslips(request):
    """
    My payslips view
    عرض قسائم رواتبي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    payslips = Payslip.objects.filter(
        employee=request.user.employee_profile
    ).select_related('payroll').order_by('-payroll__year', '-payroll__month')
    
    context = {
        'payslips': payslips,
    }
    
    return render(request, 'payroll/my_payslips.html', context)


@login_required
def payslip_detail(request, pk):
    """
    Payslip detail view
    عرض تفاصيل قسيمة الراتب
    """
    payslip = get_object_or_404(Payslip, pk=pk)
    
    # Check permission
    if not request.user.is_superuser and hasattr(request.user, 'employee_profile'):
        if payslip.employee != request.user.employee_profile:
            messages.error(request, 'ليس لديك صلاحية لعرض هذه القسيمة.')
            return redirect('payroll:my_payslips')
    
    return render(request, 'payroll/payslip_detail.html', {'payslip': payslip})


@login_required
def payslip_create(request, payroll_pk):
    """
    Payslip create view
    عرض إضافة قسيمة راتب
    """
    payroll = get_object_or_404(Payroll, pk=payroll_pk)
    
    if request.method == 'POST':
        form = PayslipForm(request.POST)
        if form.is_valid():
            payslip = form.save(commit=False)
            payslip.payroll = payroll
            payslip.save()
            messages.success(request, 'تم إضافة قسيمة الراتب بنجاح.')
            return redirect('payroll:payroll_detail', pk=payroll.pk)
    else:
        form = PayslipForm(initial={'payroll': payroll})
    
    return render(request, 'payroll/payslip_form.html', {'form': form, 'payroll': payroll})


# Loan Views
@login_required
def loan_list(request):
    """
    Loan list view
    عرض قائمة القروض
    """
    loans = Loan.objects.select_related('employee').all().order_by('-start_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        loans = loans.filter(status=status)
    
    # Pagination
    paginator = Paginator(loans, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'payroll/loan_list.html', context)


@login_required
def loan_detail(request, pk):
    """
    Loan detail view
    عرض تفاصيل القرض
    """
    loan = get_object_or_404(Loan, pk=pk)
    return render(request, 'payroll/loan_detail.html', {'loan': loan})


@login_required
def loan_create(request):
    """
    Loan create view
    عرض طلب قرض
    """
    if request.method == 'POST':
        form = LoanForm(request.POST, user=request.user)
        if form.is_valid():
            loan = form.save()
            messages.success(request, 'تم إرسال طلب القرض بنجاح.')
            return redirect('payroll:loan_list')
    else:
        form = LoanForm(user=request.user)
    
    return render(request, 'payroll/loan_form.html', {'form': form})


@login_required
def loan_approve(request, pk):
    """
    Loan approve view
    عرض الموافقة على القرض
    """
    loan = get_object_or_404(Loan, pk=pk)
    
    if request.method == 'POST':
        loan.status = 'approved'
        loan.save()
        messages.success(request, 'تمت الموافقة على القرض بنجاح.')
        return redirect('payroll:loan_detail', pk=loan.pk)
    
    return render(request, 'payroll/loan_approve.html', {'loan': loan})


# Bonus Views
@login_required
def bonus_list(request):
    """
    Bonus list view
    عرض قائمة المكافآت
    """
    bonuses = Bonus.objects.select_related('employee').all().order_by('-date')
    
    # Pagination
    paginator = Paginator(bonuses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'payroll/bonus_list.html', context)


@login_required
def bonus_create(request):
    """
    Bonus create view
    عرض إضافة مكافأة
    """
    if request.method == 'POST':
        form = BonusForm(request.POST)
        if form.is_valid():
            bonus = form.save()
            messages.success(request, 'تم إضافة المكافأة بنجاح.')
            return redirect('payroll:bonus_list')
    else:
        form = BonusForm()
    
    return render(request, 'payroll/bonus_form.html', {'form': form})

