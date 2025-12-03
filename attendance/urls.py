"""
URL configuration for attendance app
إعدادات URL لتطبيق الحضور
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('add/', views.attendance_create, name='attendance_create'),
    path('today/', views.attendance_today, name='attendance_today'),
    path('<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('leave-requests/', views.leave_request_list, name='leave_request_list'),
    path('leave-requests/mine/', views.my_leave_requests, name='my_leave_requests'),
    path('leave-requests/<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('leave-requests/add/', views.leave_request_create, name='leave_request_create'),
    path('leave-requests/<int:pk>/approve/', views.leave_request_approve, name='leave_request_approve'),
    path('leave-requests/<int:pk>/reject/', views.leave_request_reject, name='leave_request_reject'),
    path('overtime/', views.overtime_list, name='overtime_list'),
    path('overtime/add/', views.overtime_create, name='overtime_create'),
    path('zk-sync/', views.zk_sync, name='zk_sync'),
    path('zk-test-connection/', views.zk_test_connection, name='zk_test_connection'),
]

