from django.contrib import admin
from .models import PerformanceReviewCycle, PerformanceReview, KPI, EmployeeKPI, Goal

admin.site.register(PerformanceReviewCycle)
admin.site.register(PerformanceReview)
admin.site.register(KPI)
admin.site.register(EmployeeKPI)
admin.site.register(Goal)

