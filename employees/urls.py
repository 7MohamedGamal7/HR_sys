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
    path('<int:pk>/activate/', views.employee_activate, name='employee_activate'),
    path('<int:pk>/deactivate/', views.employee_deactivate, name='employee_deactivate'),
    
    # Employee Documents
    path('<int:employee_pk>/documents/', views.employee_documents, name='employee_documents'),
    path('<int:employee_pk>/documents/add/', views.document_create, name='document_create'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    
    # Employee Contracts
    path('<int:employee_pk>/contracts/', views.employee_contracts, name='employee_contracts'),
    path('<int:employee_pk>/contracts/add/', views.contract_create, name='contract_create'),
    path('contracts/<int:pk>/edit/', views.contract_update, name='contract_update'),
    path('contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),
    
    # Emergency Contacts
    path('<int:employee_pk>/emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    path('<int:employee_pk>/emergency-contacts/add/', views.emergency_contact_create, name='emergency_contact_create'),
    path('emergency-contacts/<int:pk>/edit/', views.emergency_contact_update, name='emergency_contact_update'),
    path('emergency-contacts/<int:pk>/delete/', views.emergency_contact_delete, name='emergency_contact_delete'),
    
    # Education
    path('<int:employee_pk>/education/', views.employee_education, name='employee_education'),
    path('<int:employee_pk>/education/add/', views.education_create, name='education_create'),
    path('education/<int:pk>/edit/', views.education_update, name='education_update'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),
    
    # Experience
    path('<int:employee_pk>/experience/', views.employee_experience, name='employee_experience'),
    path('<int:employee_pk>/experience/add/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_update, name='experience_update'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    
    # Export
    path('export/excel/', views.export_employees_excel, name='export_employees_excel'),
    path('export/pdf/', views.export_employees_pdf, name='export_employees_pdf'),
]

