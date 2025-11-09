"""
URL configuration for payroll app
إعدادات URL لتطبيق الرواتب
"""
from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Payroll
    path('', views.payroll_list, name='payroll_list'),
    path('generate/', views.payroll_generate, name='payroll_generate'),
    path('<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('<int:pk>/edit/', views.payroll_update, name='payroll_update'),
    path('<int:pk>/approve/', views.payroll_approve, name='payroll_approve'),
    path('<int:pk>/pay/', views.payroll_pay, name='payroll_pay'),
    path('<int:pk>/delete/', views.payroll_delete, name='payroll_delete'),
    
    # Payslips
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslips/my/', views.my_payslips, name='my_payslips'),
    path('payslips/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('payslips/<int:pk>/download/', views.payslip_download, name='payslip_download'),
    path('payslips/<int:pk>/send/', views.payslip_send, name='payslip_send'),
    
    # Loans
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/my/', views.my_loans, name='my_loans'),
    path('loans/add/', views.loan_create, name='loan_create'),
    path('loans/<int:pk>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:pk>/edit/', views.loan_update, name='loan_update'),
    path('loans/<int:pk>/approve/', views.loan_approve, name='loan_approve'),
    path('loans/<int:pk>/reject/', views.loan_reject, name='loan_reject'),
    
    # Bonuses
    path('bonuses/', views.bonus_list, name='bonus_list'),
    path('bonuses/add/', views.bonus_create, name='bonus_create'),
    path('bonuses/<int:pk>/edit/', views.bonus_update, name='bonus_update'),
    path('bonuses/<int:pk>/delete/', views.bonus_delete, name='bonus_delete'),
    
    # Reports
    path('reports/summary/', views.payroll_summary_report, name='payroll_summary_report'),
    path('reports/detailed/', views.payroll_detailed_report, name='payroll_detailed_report'),
]

