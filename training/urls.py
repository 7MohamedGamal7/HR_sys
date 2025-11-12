"""
URL configuration for training app
إعدادات URL لتطبيق التدريب
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'training'

def placeholder_view(request):
    return HttpResponse("Training module - Under development")

urlpatterns = [
    path('', placeholder_view, name='program_list'),
]

