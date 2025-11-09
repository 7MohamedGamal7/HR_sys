"""
URL configuration for performance app
إعدادات URL لتطبيق تقييم الأداء
"""
from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    # Performance Reviews
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/my/', views.my_reviews, name='my_reviews'),
    path('reviews/add/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/', views.review_detail, name='review_detail'),
    path('reviews/<int:pk>/edit/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/submit/', views.review_submit, name='review_submit'),
    path('reviews/<int:pk>/approve/', views.review_approve, name='review_approve'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    
    # KPIs
    path('kpis/', views.kpi_list, name='kpi_list'),
    path('kpis/add/', views.kpi_create, name='kpi_create'),
    path('kpis/<int:pk>/edit/', views.kpi_update, name='kpi_update'),
    path('kpis/<int:pk>/delete/', views.kpi_delete, name='kpi_delete'),
    
    # Goals
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/my/', views.my_goals, name='my_goals'),
    path('goals/add/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:pk>/edit/', views.goal_update, name='goal_update'),
    path('goals/<int:pk>/complete/', views.goal_complete, name='goal_complete'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    
    # Reports
    path('reports/summary/', views.performance_summary, name='performance_summary'),
    path('reports/employee/<int:employee_pk>/', views.employee_performance, name='employee_performance'),
]

