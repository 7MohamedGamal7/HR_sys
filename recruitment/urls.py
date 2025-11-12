"""
URL configuration for recruitment app
إعدادات URL لتطبيق التوظيف
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'recruitment'

def placeholder_view(request):
    return HttpResponse("Recruitment module - Under development")

urlpatterns = [
    path('', placeholder_view, name='job_list'),
]

