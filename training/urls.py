"""
URL configuration for training app
إعدادات URL لتطبيق التدريب
"""
from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Training Program URLs
    path('', views.program_list, name='program_list'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('program/create/', views.program_create, name='program_create'),
    path('program/<int:pk>/update/', views.program_update, name='program_update'),

    # Training Session URLs
    path('sessions/', views.session_list, name='session_list'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('session/create/', views.session_create, name='session_create'),
    path('program/<int:program_pk>/session/create/', views.session_create, name='session_create_for_program'),
    path('session/<int:pk>/update/', views.session_update, name='session_update'),

    # Training Enrollment URLs
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('session/<int:session_pk>/enroll/', views.enrollment_create, name='enrollment_create'),
]

