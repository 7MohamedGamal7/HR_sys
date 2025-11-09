"""
URL configuration for training app
إعدادات URL لتطبيق التدريب
"""
from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Training Programs
    path('programs/', views.program_list, name='program_list'),
    path('programs/add/', views.program_create, name='program_create'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('programs/<int:pk>/edit/', views.program_update, name='program_update'),
    path('programs/<int:pk>/delete/', views.program_delete, name='program_delete'),
    
    # Training Sessions
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/add/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    path('sessions/<int:pk>/edit/', views.session_update, name='session_update'),
    path('sessions/<int:pk>/complete/', views.session_complete, name='session_complete'),
    path('sessions/<int:pk>/cancel/', views.session_cancel, name='session_cancel'),
    
    # Enrollments
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/my/', views.my_enrollments, name='my_enrollments'),
    path('enrollments/add/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/complete/', views.enrollment_complete, name='enrollment_complete'),
    path('enrollments/<int:pk>/cancel/', views.enrollment_cancel, name='enrollment_cancel'),
    
    # Reports
    path('reports/summary/', views.training_summary, name='training_summary'),
    path('reports/employee/<int:employee_pk>/', views.employee_training, name='employee_training'),
]

