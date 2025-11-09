"""
URL configuration for reports app
إعدادات URL لتطبيق التقارير
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard
    path('', views.reports_dashboard, name='reports_dashboard'),
    
    # Employee Reports
    path('employees/summary/', views.employee_summary_report, name='employee_summary_report'),
    path('employees/detailed/', views.employee_detailed_report, name='employee_detailed_report'),
    path('employees/turnover/', views.employee_turnover_report, name='employee_turnover_report'),
    
    # Attendance Reports
    path('attendance/daily/', views.attendance_daily_report, name='attendance_daily_report'),
    path('attendance/monthly/', views.attendance_monthly_report, name='attendance_monthly_report'),
    path('attendance/late/', views.attendance_late_report, name='attendance_late_report'),
    path('attendance/absent/', views.attendance_absent_report, name='attendance_absent_report'),
    
    # Leave Reports
    path('leaves/summary/', views.leave_summary_report, name='leave_summary_report'),
    path('leaves/balance/', views.leave_balance_report, name='leave_balance_report'),
    
    # Payroll Reports
    path('payroll/summary/', views.payroll_summary_report, name='payroll_summary_report'),
    path('payroll/detailed/', views.payroll_detailed_report, name='payroll_detailed_report'),
    path('payroll/tax/', views.payroll_tax_report, name='payroll_tax_report'),
    
    # Performance Reports
    path('performance/summary/', views.performance_summary_report, name='performance_summary_report'),
    path('performance/kpi/', views.performance_kpi_report, name='performance_kpi_report'),
    
    # Custom Reports
    path('custom/', views.custom_report, name='custom_report'),
    path('custom/generate/', views.generate_custom_report, name='generate_custom_report'),
]

