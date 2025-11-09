"""
Views for training app
عرض تطبيق التدريب
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import TrainingProgram, TrainingSession, TrainingEnrollment
from .forms import TrainingProgramForm, TrainingSessionForm, TrainingEnrollmentForm


# Training Program Views
@login_required
def program_list(request):
    """
    Training program list view
    عرض قائمة البرامج التدريبية
    """
    programs = TrainingProgram.objects.filter(is_active=True).order_by('name')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        programs = programs.filter(category=category)
    
    context = {
        'programs': programs,
    }
    
    return render(request, 'training/program_list.html', context)


@login_required
def program_detail(request, pk):
    """
    Training program detail view
    عرض تفاصيل البرنامج التدريبي
    """
    program = get_object_or_404(TrainingProgram, pk=pk)
    sessions = TrainingSession.objects.filter(program=program).order_by('-start_date')
    
    context = {
        'program': program,
        'sessions': sessions,
    }
    
    return render(request, 'training/program_detail.html', context)


@login_required
def program_create(request):
    """
    Training program create view
    عرض إضافة برنامج تدريبي
    """
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'تم إضافة البرنامج التدريبي بنجاح.')
            return redirect('training:program_detail', pk=program.pk)
    else:
        form = TrainingProgramForm()
    
    return render(request, 'training/program_form.html', {'form': form})


@login_required
def program_update(request, pk):
    """
    Training program update view
    عرض تعديل البرنامج التدريبي
    """
    program = get_object_or_404(TrainingProgram, pk=pk)
    
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'تم تحديث البرنامج التدريبي بنجاح.')
            return redirect('training:program_detail', pk=program.pk)
    else:
        form = TrainingProgramForm(instance=program)
    
    return render(request, 'training/program_form.html', {'form': form, 'program': program})


# Training Session Views
@login_required
def session_list(request):
    """
    Training session list view
    عرض قائمة الجلسات التدريبية
    """
    sessions = TrainingSession.objects.select_related('program', 'trainer').all().order_by('-start_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        sessions = sessions.filter(status=status)
    
    # Pagination
    paginator = Paginator(sessions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'training/session_list.html', context)


@login_required
def session_detail(request, pk):
    """
    Training session detail view
    عرض تفاصيل الجلسة التدريبية
    """
    session = get_object_or_404(TrainingSession, pk=pk)
    enrollments = TrainingEnrollment.objects.filter(session=session).select_related('employee')
    
    context = {
        'session': session,
        'enrollments': enrollments,
    }
    
    return render(request, 'training/session_detail.html', context)


@login_required
def session_create(request, program_pk=None):
    """
    Training session create view
    عرض إضافة جلسة تدريبية
    """
    program = None
    if program_pk:
        program = get_object_or_404(TrainingProgram, pk=program_pk)
    
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            messages.success(request, 'تم إضافة الجلسة التدريبية بنجاح.')
            return redirect('training:session_detail', pk=session.pk)
    else:
        initial = {'program': program} if program else {}
        form = TrainingSessionForm(initial=initial)
    
    return render(request, 'training/session_form.html', {'form': form, 'program': program})


@login_required
def session_update(request, pk):
    """
    Training session update view
    عرض تعديل الجلسة التدريبية
    """
    session = get_object_or_404(TrainingSession, pk=pk)
    
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save()
            messages.success(request, 'تم تحديث الجلسة التدريبية بنجاح.')
            return redirect('training:session_detail', pk=session.pk)
    else:
        form = TrainingSessionForm(instance=session)
    
    return render(request, 'training/session_form.html', {'form': form, 'session': session})


# Training Enrollment Views
@login_required
def enrollment_list(request):
    """
    Training enrollment list view
    عرض قائمة التسجيلات التدريبية
    """
    enrollments = TrainingEnrollment.objects.select_related('session', 'employee').all().order_by('-enrollment_date')
    
    # Pagination
    paginator = Paginator(enrollments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'training/enrollment_list.html', context)


@login_required
def my_enrollments(request):
    """
    My training enrollments view
    عرض تدريباتي
    """
    if not hasattr(request.user, 'employee_profile'):
        messages.error(request, 'لا يوجد ملف موظف مرتبط بحسابك.')
        return redirect('core:dashboard')
    
    enrollments = TrainingEnrollment.objects.filter(
        employee=request.user.employee_profile
    ).select_related('session', 'session__program').order_by('-enrollment_date')
    
    context = {
        'enrollments': enrollments,
    }
    
    return render(request, 'training/my_enrollments.html', context)


@login_required
def enrollment_create(request, session_pk):
    """
    Training enrollment create view
    عرض التسجيل في تدريب
    """
    session = get_object_or_404(TrainingSession, pk=session_pk)
    
    if request.method == 'POST':
        form = TrainingEnrollmentForm(request.POST, user=request.user)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.session = session
            enrollment.save()
            messages.success(request, 'تم التسجيل في التدريب بنجاح.')
            return redirect('training:my_enrollments')
    else:
        form = TrainingEnrollmentForm(user=request.user, initial={'session': session})
    
    return render(request, 'training/enrollment_form.html', {'form': form, 'session': session})

