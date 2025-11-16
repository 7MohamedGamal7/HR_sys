from django.contrib import admin
from .models import JobPosting, JobApplication, Interview, JobOffer, OnboardingTask

admin.site.register(JobPosting)
admin.site.register(JobApplication)
admin.site.register(Interview)
admin.site.register(JobOffer)
admin.site.register(OnboardingTask)

