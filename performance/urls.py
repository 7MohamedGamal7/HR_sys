"""
URL configuration for performance app
إعدادات URL لتطبيق تقييم الأداء
"""
from django.urls import path
from django.http import HttpResponse

app_name = 'performance'

def placeholder_view(request):
    return HttpResponse("Performance module - Under development")

urlpatterns = [
    path('', placeholder_view, name='review_list'),
]

