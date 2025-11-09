from django.contrib import admin
from .models import JobPosting, JobApplication, Interview, OnboardingTask

admin.site.register(JobPosting)
admin.site.register(JobApplication)
admin.site.register(Interview)
admin.site.register(OnboardingTask)

