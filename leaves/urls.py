"""
URL configuration for leaves app
إعدادات URL لتطبيق الإجازات
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'leaves'

def placeholder_view(request):
    return HttpResponse("Leaves module - Under development")

urlpatterns = [
    path('', placeholder_view, name='leaves_list'),
]

