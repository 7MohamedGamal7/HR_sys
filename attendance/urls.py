"""
URL configuration for attendance app
إعدادات URL لتطبيق الحضور
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Attendance
    path('', views.attendance_list, name='attendance_list'),
    path('today/', views.attendance_today, name='attendance_today'),
    path('add/', views.attendance_create, name='attendance_create'),
    path('<int:pk>/edit/', views.attendance_update, name='attendance_update'),
    path('<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('employee/<int:employee_pk>/', views.employee_attendance, name='employee_attendance'),
    
    # ZK Device Management
    path('zk/devices/', views.zk_devices, name='zk_devices'),
    path('zk/sync/', views.zk_sync, name='zk_sync'),
    path('zk/sync/status/', views.zk_sync_status, name='zk_sync_status'),
    path('zk/test/<str:device_ip>/', views.zk_test_device, name='zk_test_device'),
    path('zk/logs/', views.attendance_logs, name='attendance_logs'),
    path('zk/logs/process/', views.process_logs, name='process_logs'),
    
    # Leave Requests
    path('leaves/', views.leave_request_list, name='leave_request_list'),
    path('leaves/my/', views.my_leave_requests, name='my_leave_requests'),
    path('leaves/add/', views.leave_request_create, name='leave_request_create'),
    path('leaves/<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('leaves/<int:pk>/edit/', views.leave_request_update, name='leave_request_update'),
    path('leaves/<int:pk>/cancel/', views.leave_request_cancel, name='leave_request_cancel'),
    path('leaves/<int:pk>/approve/', views.leave_request_approve, name='leave_request_approve'),
    path('leaves/<int:pk>/reject/', views.leave_request_reject, name='leave_request_reject'),
    
    # Overtime
    path('overtime/', views.overtime_list, name='overtime_list'),
    path('overtime/add/', views.overtime_create, name='overtime_create'),
    path('overtime/<int:pk>/edit/', views.overtime_update, name='overtime_update'),
    path('overtime/<int:pk>/approve/', views.overtime_approve, name='overtime_approve'),
    path('overtime/<int:pk>/reject/', views.overtime_reject, name='overtime_reject'),
    
    # Reports
    path('reports/daily/', views.daily_attendance_report, name='daily_attendance_report'),
    path('reports/monthly/', views.monthly_attendance_report, name='monthly_attendance_report'),
    path('reports/employee/', views.employee_attendance_report, name='employee_attendance_report'),
    path('reports/late/', views.late_report, name='late_report'),
    path('reports/absent/', views.absent_report, name='absent_report'),
]

