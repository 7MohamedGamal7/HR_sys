"""
URL configuration for HR_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hr_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employees/', views.employees_view, name='employees'),
    path('employees/<int:emp_id>/', views.employee_detail_view, name='view_employee'),
    path('employees/add/', views.add_employee_view, name='add_employee'),
    path('employees/<int:emp_id>/edit/', views.edit_employee_view, name='edit_employee'),
    path('employees/<int:emp_id>/delete/', views.delete_employee_view, name='delete_employee'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('leaves/', views.leaves_view, name='leaves'),
    path('leaves/apply/', views.apply_leave_view, name='apply_leave'),
    path('leaves/<int:leave_id>/approve/', views.approve_leave_view, name='approve_leave'),
    path('leaves/<int:leave_id>/reject/', views.reject_leave_view, name='reject_leave'),
    path('payroll/', views.payroll_view, name='payroll'),
    path('payroll/<int:payslip_id>/edit/', views.edit_payslip_view, name='edit_payslip'),
    path('payroll/<int:payslip_id>/delete/', views.delete_payslip_view, name='delete_payslip'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
]