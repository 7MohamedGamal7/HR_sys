"""
URL configuration for reports app
إعدادات URL لتطبيق التقارير
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'reports'

def placeholder_view(request):
    return HttpResponse("Reports module - Under development")

urlpatterns = [
    path('', placeholder_view, name='reports_dashboard'),
]

