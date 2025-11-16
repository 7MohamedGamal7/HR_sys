"""
URL configuration for reports app
إعدادات URL لتطبيق التقارير
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Reports Dashboard
    path('', views.reports_dashboard, name='reports_dashboard'),

    # Employee Reports
    path('employee-summary/', views.employee_summary_report, name='employee_summary_report'),

    # Attendance Reports
    path('attendance-summary/', views.attendance_summary_report, name='attendance_summary_report'),
    path('attendance-monthly/', views.attendance_monthly_report, name='attendance_monthly_report'),

    # Leave Reports
    path('leave-summary/', views.leave_summary_report, name='leave_summary_report'),

    # Payroll Reports
    path('payroll-summary/', views.payroll_summary_report, name='payroll_summary_report'),
]

