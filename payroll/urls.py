"""
URL configuration for payroll app
إعدادات URL لتطبيق الرواتب
"""
from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    # Payroll URLs
    path('', views.payroll_list, name='payroll_list'),
    path('payroll/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('payroll/create/', views.payroll_create, name='payroll_create'),

    # Payslip URLs
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('my-payslips/', views.my_payslips, name='my_payslips'),
    path('payslip/<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('payroll/<int:payroll_pk>/payslip/create/', views.payslip_create, name='payslip_create'),

    # Loan URLs
    path('loans/', views.loan_list, name='loan_list'),
    path('loan/<int:pk>/', views.loan_detail, name='loan_detail'),
    path('loan/create/', views.loan_create, name='loan_create'),
    path('loan/<int:pk>/approve/', views.loan_approve, name='loan_approve'),

    # Bonus URLs
    path('bonuses/', views.bonus_list, name='bonus_list'),
    path('bonus/create/', views.bonus_create, name='bonus_create'),
]

