from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('donations/', views.manage_donations, name='manage_donations'),
    path('donations/<int:pk>/approve/', views.approve_donation, name='approve_donation'),
    path('donations/<int:pk>/reject/', views.reject_donation, name='reject_donation'),
    path('requests/', views.manage_requests, name='manage_requests'),
    path('requests/<int:pk>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:pk>/reject/', views.reject_request, name='reject_request'),
    path('requests/<int:pk>/fulfill/', views.fulfill_request, name='fulfill_request'),
    path('blood-stock/', views.blood_stock, name='blood_stock'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:pk>/verify/', views.verify_user, name='verify_user'),
]