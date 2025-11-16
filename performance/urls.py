"""
URL configuration for performance app
إعدادات URL لتطبيق تقييم الأداء
"""
from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    # Performance Review URLs
    path('', views.review_list, name='review_list'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('review/create/', views.review_create, name='review_create'),
    path('review/<int:pk>/update/', views.review_update, name='review_update'),

    # KPI URLs
    path('kpis/', views.kpi_list, name='kpi_list'),
    path('kpi/create/', views.kpi_create, name='kpi_create'),
    path('kpi/<int:pk>/update/', views.kpi_update, name='kpi_update'),

    # Goal URLs
    path('goals/', views.goal_list, name='goal_list'),
    path('my-goals/', views.my_goals, name='my_goals'),
    path('goal/<int:pk>/', views.goal_detail, name='goal_detail'),
    path('goal/create/', views.goal_create, name='goal_create'),
    path('goal/<int:pk>/update/', views.goal_update, name='goal_update'),
]

