"""
URL configuration for HR_sys project
إعدادات URL لمشروع نظام الموارد البشرية
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Core App (Dashboard, Auth, Notifications, Settings)
    path('', include('core.urls')),

    # Organization Structure
    path('organization/', include('organization.urls')),

    # Employee Management
    path('employees/', include('employees.urls')),

    # Attendance & Leaves
    # path('attendance/', include('attendance.urls')),  # Temporarily disabled
    # path('leaves/', include('leaves.urls')),  # Temporarily disabled

    # Payroll
    # path('payroll/', include('payroll.urls')),  # Temporarily disabled

    # Performance Management
    # path('performance/', include('performance.urls')),  # Temporarily disabled

    # Recruitment
    # path('recruitment/', include('recruitment.urls')),  # Temporarily disabled

    # Training & Development
    # path('training/', include('training.urls')),  # Temporarily disabled

    # Reports & Analytics
    # path('reports/', include('reports.urls')),  # Temporarily disabled
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'نظام إدارة الموارد البشرية'
admin.site.site_title = 'HR Management System'
admin.site.index_title = 'لوحة التحكم'