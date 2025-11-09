"""
URL configuration for core app
إعدادات URL لتطبيق النواة
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # System Settings (Admin only)
    path('settings/', views.system_settings, name='system_settings'),
    path('settings/<int:pk>/edit/', views.edit_setting, name='edit_setting'),
    
    # Audit Log (Admin only)
    path('audit-log/', views.audit_log, name='audit_log'),
]

