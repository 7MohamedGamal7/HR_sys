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

    # Employee Insurances
    path('<int:employee_pk>/insurances/add/', views.employee_insurance_create, name='insurance_create'),

    # Employee Custody
    path('<int:employee_pk>/custody/add/', views.employee_custody_create, name='custody_create'),

    # Emergency Contacts
    path('<int:employee_pk>/emergency-contacts/add/', views.emergency_contact_create, name='emergency_contact_create'),

    # Education
    path('<int:employee_pk>/education/add/', views.employee_education_create, name='education_create'),

    # Experience
    path('<int:employee_pk>/experience/add/', views.employee_experience_create, name='experience_create'),
    
    # Photo Upload
    path('<int:pk>/photo/upload/', views.employee_photo_upload, name='photo_upload'),
    
    # Inline Update for Employee Detail Tabs
    path('<int:pk>/inline-update/', views.employee_inline_update, name='employee_inline_update'),
    
    # Individual Item Operations (Get/Delete)
    path('<str:item_type>/<int:item_id>/get/', views.employee_item_get, name='employee_item_get'),
    path('<str:item_type>/<int:item_id>/delete/', views.employee_item_delete, name='employee_item_delete'),
]

