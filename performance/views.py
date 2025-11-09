"""
Views for performance app
عرض تطبيق تقييم الأداء
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import PerformanceReview, KPI, Goal
from .forms import PerformanceReviewForm, KPIForm, GoalForm


# Performance Review Views
@login_required
def review_list(request):
    """
    Performance review list view
    عرض قائمة تقييمات الأداء
    """
    reviews = PerformanceReview.objects.select_related('employee', 'reviewer').all().order_by('-review_period_end')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        reviews = reviews.filter(status=status)
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'performance/review_list.html', context)


@login_required
def my_reviews(request):
    """
    My performance reviews view
    عرض تقييماتي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    reviews = PerformanceReview.objects.filter(
        employee=request.user.employee_profile
    ).select_related('reviewer').order_by('-review_period_end')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'performance/my_reviews.html', context)


@login_required
def review_detail(request, pk):
    """
    Performance review detail view
    عرض تفاصيل تقييم الأداء
    """
    review = get_object_or_404(PerformanceReview, pk=pk)
    return render(request, 'performance/review_detail.html', {'review': review})


@login_required
def review_create(request):
    """
    Performance review create view
    عرض إنشاء تقييم أداء
    """
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'تم إنشاء تقييم الأداء بنجاح.')
            return redirect('performance:review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm()
    
    return render(request, 'performance/review_form.html', {'form': form})


@login_required
def review_update(request, pk):
    """
    Performance review update view
    عرض تعديل تقييم الأداء
    """
    review = get_object_or_404(PerformanceReview, pk=pk)
    
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'تم تحديث تقييم الأداء بنجاح.')
            return redirect('performance:review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm(instance=review)
    
    return render(request, 'performance/review_form.html', {'form': form, 'review': review})


# KPI Views
@login_required
def kpi_list(request):
    """
    KPI list view
    عرض قائمة مؤشرات الأداء
    """
    kpis = KPI.objects.filter(is_active=True).order_by('name')
    
    context = {
        'kpis': kpis,
    }
    
    return render(request, 'performance/kpi_list.html', context)


@login_required
def kpi_create(request):
    """
    KPI create view
    عرض إضافة مؤشر أداء
    """
    if request.method == 'POST':
        form = KPIForm(request.POST)
        if form.is_valid():
            kpi = form.save()
            messages.success(request, 'تم إضافة مؤشر الأداء بنجاح.')
            return redirect('performance:kpi_list')
    else:
        form = KPIForm()
    
    return render(request, 'performance/kpi_form.html', {'form': form})


@login_required
def kpi_update(request, pk):
    """
    KPI update view
    عرض تعديل مؤشر الأداء
    """
    kpi = get_object_or_404(KPI, pk=pk)
    
    if request.method == 'POST':
        form = KPIForm(request.POST, instance=kpi)
        if form.is_valid():
            kpi = form.save()
            messages.success(request, 'تم تحديث مؤشر الأداء بنجاح.')
            return redirect('performance:kpi_list')
    else:
        form = KPIForm(instance=kpi)
    
    return render(request, 'performance/kpi_form.html', {'form': form, 'kpi': kpi})


# Goal Views
@login_required
def goal_list(request):
    """
    Goal list view
    عرض قائمة الأهداف
    """
    goals = Goal.objects.select_related('employee').all().order_by('-due_date')
    
    # Pagination
    paginator = Paginator(goals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'performance/goal_list.html', context)


@login_required
def my_goals(request):
    """
    My goals view
    عرض أهدافي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    goals = Goal.objects.filter(
        employee=request.user.employee_profile
    ).order_by('-due_date')
    
    context = {
        'goals': goals,
    }
    
    return render(request, 'performance/my_goals.html', context)


@login_required
def goal_detail(request, pk):
    """
    Goal detail view
    عرض تفاصيل الهدف
    """
    goal = get_object_or_404(Goal, pk=pk)
    return render(request, 'performance/goal_detail.html', {'goal': goal})


@login_required
def goal_create(request):
    """
    Goal create view
    عرض إضافة هدف
    """
    if request.method == 'POST':
        form = GoalForm(request.POST, user=request.user)
        if form.is_valid():
            goal = form.save()
            messages.success(request, 'تم إضافة الهدف بنجاح.')
            return redirect('performance:my_goals')
    else:
        form = GoalForm(user=request.user)
    
    return render(request, 'performance/goal_form.html', {'form': form})


@login_required
def goal_update(request, pk):
    """
    Goal update view
    عرض تعديل الهدف
    """
    goal = get_object_or_404(Goal, pk=pk)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal, user=request.user)
        if form.is_valid():
            goal = form.save()
            messages.success(request, 'تم تحديث الهدف بنجاح.')
            return redirect('performance:goal_detail', pk=goal.pk)
    else:
        form = GoalForm(instance=goal, user=request.user)
    
    return render(request, 'performance/goal_form.html', {'form': form, 'goal': goal})

