"""
URL configuration for recruitment app
إعدادات URL لتطبيق التوظيف
"""
from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    # Job Postings
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/add/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', views.job_update, name='job_update'),
    path('jobs/<int:pk>/close/', views.job_close, name='job_close'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    
    # Applications
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/shortlist/', views.application_shortlist, name='application_shortlist'),
    path('applications/<int:pk>/reject/', views.application_reject, name='application_reject'),
    
    # Interviews
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/add/', views.interview_create, name='interview_create'),
    path('interviews/<int:pk>/', views.interview_detail, name='interview_detail'),
    path('interviews/<int:pk>/edit/', views.interview_update, name='interview_update'),
    path('interviews/<int:pk>/complete/', views.interview_complete, name='interview_complete'),
    path('interviews/<int:pk>/cancel/', views.interview_cancel, name='interview_cancel'),
    
    # Offers
    path('offers/', views.offer_list, name='offer_list'),
    path('offers/add/', views.offer_create, name='offer_create'),
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('offers/<int:pk>/send/', views.offer_send, name='offer_send'),
    path('offers/<int:pk>/accept/', views.offer_accept, name='offer_accept'),
    path('offers/<int:pk>/reject/', views.offer_reject, name='offer_reject'),
]

