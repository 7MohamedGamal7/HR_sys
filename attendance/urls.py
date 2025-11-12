"""
URL configuration for attendance app
إعدادات URL لتطبيق الحضور
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Attendance - Only working views
    path('', views.attendance_list, name='attendance_list'),
    path('add/', views.attendance_create, name='attendance_create'),
]

