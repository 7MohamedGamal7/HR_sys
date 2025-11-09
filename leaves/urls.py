"""
URL configuration for leaves app
إعدادات URL لتطبيق الإجازات
"""
from django.urls import path
from . import views

app_name = 'leaves'

urlpatterns = [
    # Leave Policies
    path('policies/', views.leave_policy_list, name='leave_policy_list'),
    path('policies/add/', views.leave_policy_create, name='leave_policy_create'),
    path('policies/<int:pk>/edit/', views.leave_policy_update, name='leave_policy_update'),
    path('policies/<int:pk>/delete/', views.leave_policy_delete, name='leave_policy_delete'),
    
    # Leave Balances
    path('balances/', views.leave_balance_list, name='leave_balance_list'),
    path('balances/my/', views.my_leave_balance, name='my_leave_balance'),
    path('balances/employee/<int:employee_pk>/', views.employee_leave_balance, name='employee_leave_balance'),
    path('balances/update/', views.update_leave_balances, name='update_leave_balances'),
    
    # Leave Approval Workflow
    path('workflows/', views.leave_workflow_list, name='leave_workflow_list'),
    path('workflows/add/', views.leave_workflow_create, name='leave_workflow_create'),
    path('workflows/<int:pk>/edit/', views.leave_workflow_update, name='leave_workflow_update'),
    path('workflows/<int:pk>/delete/', views.leave_workflow_delete, name='leave_workflow_delete'),
]

