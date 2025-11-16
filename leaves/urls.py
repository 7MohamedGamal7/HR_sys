"""
URL configuration for leaves app
إعدادات URL لتطبيق الإجازات
"""
from django.urls import path
from . import views

app_name = 'leaves'

urlpatterns = [
    # Leave Policy URLs
    path('policies/', views.leave_policy_list, name='leave_policy_list'),
    path('policy/<int:pk>/', views.leave_policy_detail, name='leave_policy_detail'),
    path('policy/create/', views.leave_policy_create, name='leave_policy_create'),
    path('policy/<int:pk>/update/', views.leave_policy_update, name='leave_policy_update'),

    # Leave Balance URLs
    path('balances/', views.leave_balance_list, name='leave_balance_list'),
    path('my-balance/', views.my_leave_balance, name='my_leave_balance'),
    path('balance/create/', views.leave_balance_create, name='leave_balance_create'),
    path('balance/<int:pk>/update/', views.leave_balance_update, name='leave_balance_update'),

    # Leave Approval Workflow URLs
    path('policy/<int:policy_pk>/workflow/create/', views.workflow_create, name='workflow_create'),
]

