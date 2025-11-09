"""
URL configuration for organization app
إعدادات URL لتطبيق الهيكل التنظيمي
"""
from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # Positions
    path('positions/', views.position_list, name='position_list'),
    path('positions/add/', views.position_create, name='position_create'),
    path('positions/<int:pk>/edit/', views.position_update, name='position_update'),

    # Branches
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/add/', views.branch_create, name='branch_create'),
    path('branches/<int:pk>/edit/', views.branch_update, name='branch_update'),

    # Work Shifts
    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/add/', views.shift_create, name='shift_create'),
    path('shifts/<int:pk>/edit/', views.shift_update, name='shift_update'),

    # Holidays
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.holiday_create, name='holiday_create'),
    path('holidays/<int:pk>/edit/', views.holiday_update, name='holiday_update'),
    path('holidays/<int:pk>/delete/', views.holiday_delete, name='holiday_delete'),
]

