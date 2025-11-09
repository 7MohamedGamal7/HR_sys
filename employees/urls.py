"""
URL configuration for employees app
إعدادات URL لتطبيق الموظفين
"""
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee List and CRUD
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_create, name='employee_create'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # Employee Documents
    path('<int:employee_pk>/documents/add/', views.employee_document_create, name='document_create'),
    path('documents/<int:pk>/delete/', views.employee_document_delete, name='document_delete'),

    # Employee Contracts
    path('<int:employee_pk>/contracts/add/', views.employee_contract_create, name='contract_create'),
    path('contracts/<int:pk>/edit/', views.employee_contract_update, name='contract_update'),

    # Emergency Contacts
    path('<int:employee_pk>/emergency-contacts/add/', views.emergency_contact_create, name='emergency_contact_create'),

    # Education
    path('<int:employee_pk>/education/add/', views.employee_education_create, name='education_create'),

    # Experience
    path('<int:employee_pk>/experience/add/', views.employee_experience_create, name='experience_create'),
]

