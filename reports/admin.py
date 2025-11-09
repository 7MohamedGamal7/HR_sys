from django.contrib import admin
from .models import ReportTemplate, GeneratedReport, Dashboard

admin.site.register(ReportTemplate)
admin.site.register(GeneratedReport)
admin.site.register(Dashboard)

