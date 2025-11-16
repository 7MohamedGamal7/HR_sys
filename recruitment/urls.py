"""
URL configuration for recruitment app
إعدادات URL لتطبيق التوظيف
"""
from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    # Job Posting URLs
    path('', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/update/', views.job_update, name='job_update'),

    # Application URLs
    path('applications/', views.application_list, name='application_list'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('job/<int:job_pk>/apply/', views.application_create, name='application_create'),

    # Interview URLs
    path('interviews/', views.interview_list, name='interview_list'),
    path('interview/<int:pk>/', views.interview_detail, name='interview_detail'),
    path('application/<int:application_pk>/interview/create/', views.interview_create, name='interview_create'),

    # Job Offer URLs
    path('offers/', views.offer_list, name='offer_list'),
    path('offer/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('application/<int:application_pk>/offer/create/', views.offer_create, name='offer_create'),
]

