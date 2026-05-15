from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='requester_dashboard'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('history/', views.request_history, name='request_history'),
    path('notification/<int:pk>/read/', views.mark_notification_read, name='requester_notif_read'),
]