"""
Views for recruitment app
عرض تطبيق التوظيف
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import JobPosting, Application, Interview, JobOffer
from .forms import JobPostingForm, ApplicationForm, InterviewForm, JobOfferForm


# Job Posting Views
@login_required
def job_list(request):
    """
    Job posting list view
    عرض قائمة الوظائف
    """
    jobs = JobPosting.objects.select_related('department', 'position').all().order_by('-posting_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        jobs = jobs.filter(status=status)
    
    # Pagination
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'recruitment/job_list.html', context)


@login_required
def job_detail(request, pk):
    """
    Job posting detail view
    عرض تفاصيل الوظيفة
    """
    job = get_object_or_404(JobPosting, pk=pk)
    applications = Application.objects.filter(job_posting=job).order_by('-application_date')
    
    context = {
        'job': job,
        'applications': applications,
    }
    
    return render(request, 'recruitment/job_detail.html', context)


@login_required
def job_create(request):
    """
    Job posting create view
    عرض إضافة وظيفة
    """
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, 'تم إضافة الوظيفة بنجاح.')
            return redirect('recruitment:job_detail', pk=job.pk)
    else:
        form = JobPostingForm()
    
    return render(request, 'recruitment/job_form.html', {'form': form})


@login_required
def job_update(request, pk):
    """
    Job posting update view
    عرض تعديل الوظيفة
    """
    job = get_object_or_404(JobPosting, pk=pk)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            messages.success(request, 'تم تحديث الوظيفة بنجاح.')
            return redirect('recruitment:job_detail', pk=job.pk)
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'recruitment/job_form.html', {'form': form, 'job': job})


# Application Views
@login_required
def application_list(request):
    """
    Application list view
    عرض قائمة الطلبات
    """
    applications = Application.objects.select_related('job_posting').all().order_by('-application_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    # Pagination
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'recruitment/application_list.html', context)


@login_required
def application_detail(request, pk):
    """
    Application detail view
    عرض تفاصيل الطلب
    """
    application = get_object_or_404(Application, pk=pk)
    interviews = Interview.objects.filter(application=application).order_by('-interview_date')
    
    context = {
        'application': application,
        'interviews': interviews,
    }
    
    return render(request, 'recruitment/application_detail.html', context)


@login_required
def application_create(request, job_pk):
    """
    Application create view
    عرض إضافة طلب توظيف
    """
    job = get_object_or_404(JobPosting, pk=job_pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_posting = job
            application.save()
            messages.success(request, 'تم إرسال الطلب بنجاح.')
            return redirect('recruitment:application_detail', pk=application.pk)
    else:
        form = ApplicationForm(initial={'job_posting': job})
    
    return render(request, 'recruitment/application_form.html', {'form': form, 'job': job})


# Interview Views
@login_required
def interview_list(request):
    """
    Interview list view
    عرض قائمة المقابلات
    """
    interviews = Interview.objects.select_related('application', 'interviewer').all().order_by('-interview_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        interviews = interviews.filter(status=status)
    
    # Pagination
    paginator = Paginator(interviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'recruitment/interview_list.html', context)


@login_required
def interview_detail(request, pk):
    """
    Interview detail view
    عرض تفاصيل المقابلة
    """
    interview = get_object_or_404(Interview, pk=pk)
    return render(request, 'recruitment/interview_detail.html', {'interview': interview})


@login_required
def interview_create(request, application_pk):
    """
    Interview create view
    عرض جدولة مقابلة
    """
    application = get_object_or_404(Application, pk=application_pk)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, 'تم جدولة المقابلة بنجاح.')
            return redirect('recruitment:interview_detail', pk=interview.pk)
    else:
        form = InterviewForm(initial={'application': application})
    
    return render(request, 'recruitment/interview_form.html', {'form': form, 'application': application})


# Job Offer Views
@login_required
def offer_list(request):
    """
    Job offer list view
    عرض قائمة عروض العمل
    """
    offers = JobOffer.objects.select_related('application', 'position').all().order_by('-offer_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        offers = offers.filter(status=status)
    
    # Pagination
    paginator = Paginator(offers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'recruitment/offer_list.html', context)


@login_required
def offer_detail(request, pk):
    """
    Job offer detail view
    عرض تفاصيل عرض العمل
    """
    offer = get_object_or_404(JobOffer, pk=pk)
    return render(request, 'recruitment/offer_detail.html', {'offer': offer})


@login_required
def offer_create(request, application_pk):
    """
    Job offer create view
    عرض إنشاء عرض عمل
    """
    application = get_object_or_404(Application, pk=application_pk)
    
    if request.method == 'POST':
        form = JobOfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.application = application
            offer.save()
            messages.success(request, 'تم إنشاء عرض العمل بنجاح.')
            return redirect('recruitment:offer_detail', pk=offer.pk)
    else:
        form = JobOfferForm(initial={'application': application})
    
    return render(request, 'recruitment/offer_form.html', {'form': form, 'application': application})

