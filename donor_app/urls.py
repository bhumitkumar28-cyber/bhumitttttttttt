from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='donor_dashboard'),
    path('donate/', views.donate, name='donate'),
    path('history/', views.donation_history, name='donation_history'),
    path('notification/<int:pk>/read/', views.mark_notification_read, name='donor_notif_read'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path('notifications/', views.donor_notifications, name='donor_notifications'),
    path('settings/', views.donor_settings, name='donor_settings'),
]