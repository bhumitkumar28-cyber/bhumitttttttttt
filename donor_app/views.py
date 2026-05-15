from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from public_app.models import Donation, Notification, BloodStock
from .forms import DonationForm


def donor_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'donor':
            messages.error(request, 'Access denied.')
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@donor_required
def dashboard(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    stats = {
        'total': donations.count(),
        'approved': donations.filter(status='approved').count(),
        'pending': donations.filter(status='pending').count(),
        'rejected': donations.filter(status='rejected').count(),
    }
    return render(request, 'donor_app/dashboard.html', {
        'donations': donations[:5],
        'stats': stats,
        'notifications': notifications,
    })


@donor_required
def donate(request):
    form = DonationForm(request.POST or None, initial={'blood_group': request.user.blood_group, 'city': request.user.city})
    if request.method == 'POST' and form.is_valid():
        donation = form.save(commit=False)
        donation.donor = request.user
        donation.save()
        Notification.objects.create(
            user=request.user,
            title='Donation Submitted',
            message=f'Your donation of {donation.units} unit(s) of {donation.blood_group} blood has been submitted for approval.'
        )
        messages.success(request, 'Donation submitted successfully! Awaiting approval.')
        return redirect('donor_dashboard')
    return render(request, 'donor_app/donate.html', {'form': form})


@donor_required
def donation_history(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'donor_app/donation_history.html', {'donations': donations})


@donor_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('donor_dashboard')


def donor_profile(request):
    return render(request, 'donor_app/donor_profile.html')
@donor_required
def donor_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'donor_app/donor_notifications.html', {
        'notifications': notifications
    })
@donor_required
def donor_settings(request):
    return render(request, 'donor_app/donor_settings.html')
@donor_required
def donor_profile(request):
    total_donations = Donation.objects.filter(donor=request.user).count()
    lives_saved = total_donations * 3

    return render(request, 'donor_app/donor_profile.html', {
        'lives_saved': lives_saved,
        'donations': {
            'total': total_donations
        }
    })