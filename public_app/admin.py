from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BloodStock, Donation, BloodRequest, Notification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'blood_group', 'city', 'is_verified', 'created_at']
    list_filter = ['role', 'blood_group', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'blood_group', 'city', 'phone', 'profile_image', 'is_verified')}),
    )


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ['blood_group', 'units_available', 'updated_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_group', 'units', 'status', 'donation_date', 'created_at']
    list_filter = ['status', 'blood_group']
    actions = ['approve_donations']

    def approve_donations(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='approved', approved_at=timezone.now())
    approve_donations.short_description = 'Approve selected donations'


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'blood_group', 'units_needed', 'urgency', 'status', 'required_by']
    list_filter = ['status', 'blood_group', 'urgency']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']