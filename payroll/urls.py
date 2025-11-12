"""
URL configuration for payroll app
إعدادات URL لتطبيق الرواتب
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'payroll'

def placeholder_view(request):
    return HttpResponse("Payroll module - Under development")

urlpatterns = [
    path('', placeholder_view, name='payroll_list'),
]

