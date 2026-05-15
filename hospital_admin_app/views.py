from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from public_app.models import CustomUser, Donation, BloodRequest, BloodStock, Notification
from .forms import StockUpdateForm


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'hospital_admin':
            messages.error(request, 'Access denied. Hospital Admin only.')
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_required
def dashboard(request):
    stats = {
        'total_donors': CustomUser.objects.filter(role='donor').count(),
        'verified_donors': CustomUser.objects.filter(role='donor', is_verified=True).count(),
        'total_requesters': CustomUser.objects.filter(role='requester').count(),
        'pending_donations': Donation.objects.filter(status='pending').count(),
        'pending_requests': BloodRequest.objects.filter(status='pending').count(),
        'approved_donations': Donation.objects.filter(status='approved').count(),
        'approved_requests': BloodRequest.objects.filter(status='approved').count(),
    }
    recent_donations = Donation.objects.order_by('-created_at')[:5]
    recent_requests = BloodRequest.objects.order_by('-created_at')[:5]
    stocks = BloodStock.objects.all()
    return render(request, 'hospital_admin_app/dashboard.html', {
        'stats': stats,
        'recent_donations': recent_donations,
        'recent_requests': recent_requests,
        'stocks': stocks,
    })


@admin_required
def manage_donations(request):
    status = request.GET.get('status', '')
    donations = Donation.objects.all().order_by('-created_at')
    if status:
        donations = donations.filter(status=status)
    return render(request, 'hospital_admin_app/manage_donations.html', {
        'donations': donations,
        'current_status': status,
    })


@admin_required
def approve_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation.status = 'approved'
    donation.approved_at = timezone.now()
    donation.save()
    # Update blood stock
    stock, created = BloodStock.objects.get_or_create(blood_group=donation.blood_group, defaults={'units_available': 0})
    stock.units_available += donation.units
    stock.save()
    # Notify donor
    Notification.objects.create(
        user=donation.donor,
        title='Donation Approved',
        message=f'Your donation of {donation.units} unit(s) of {donation.blood_group} has been approved and added to the blood bank.'
    )
    # Verify donor
    donation.donor.is_verified = True
    donation.donor.save()
    messages.success(request, f'Donation approved and {donation.units} units of {donation.blood_group} added to stock.')
    return redirect('manage_donations')


@admin_required
def reject_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation.status = 'rejected'
    donation.save()
    Notification.objects.create(
        user=donation.donor,
        title='Donation Rejected',
        message=f'Your donation of {donation.units} unit(s) of {donation.blood_group} has been rejected. Please contact the hospital for more information.'
    )
    messages.warning(request, 'Donation rejected.')
    return redirect('manage_donations')


@admin_required
def manage_requests(request):
    status = request.GET.get('status', '')
    requests = BloodRequest.objects.all().order_by('-created_at')
    if status:
        requests = requests.filter(status=status)
    return render(request, 'hospital_admin_app/manage_requests.html', {
        'requests': requests,
        'current_status': status,
    })


@admin_required
def approve_request(request, pk):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    # Check stock
    try:
        stock = BloodStock.objects.get(blood_group=blood_req.blood_group)
        if stock.units_available >= blood_req.units_needed:
            stock.units_available -= blood_req.units_needed
            stock.save()
            blood_req.status = 'approved'
            blood_req.approved_at = timezone.now()
            blood_req.save()
            Notification.objects.create(
                user=blood_req.requester,
                title='Blood Request Approved',
                message=f'Your request for {blood_req.units_needed} unit(s) of {blood_req.blood_group} has been approved.'
            )
            messages.success(request, 'Blood request approved and stock updated.')
        else:
            messages.error(request, f'Insufficient stock. Available: {stock.units_available} units of {blood_req.blood_group}.')
    except BloodStock.DoesNotExist:
        messages.error(request, f'No stock available for {blood_req.blood_group}.')
    return redirect('manage_requests')


@admin_required
def reject_request(request, pk):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    blood_req.status = 'rejected'
    blood_req.save()
    Notification.objects.create(
        user=blood_req.requester,
        title='Blood Request Rejected',
        message=f'Your request for {blood_req.units_needed} unit(s) of {blood_req.blood_group} has been rejected.'
    )
    messages.warning(request, 'Blood request rejected.')
    return redirect('manage_requests')


@admin_required
def fulfill_request(request, pk):
    blood_req = get_object_or_404(BloodRequest, pk=pk)
    blood_req.status = 'fulfilled'
    blood_req.save()
    Notification.objects.create(
        user=blood_req.requester,
        title='Blood Request Fulfilled',
        message=f'Your blood request has been fulfilled. Please collect {blood_req.units_needed} unit(s) of {blood_req.blood_group} from {blood_req.hospital_name}.'
    )
    messages.success(request, 'Request marked as fulfilled.')
    return redirect('manage_requests')


@admin_required
def blood_stock(request):
    stocks = BloodStock.objects.all()
    form = StockUpdateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        bg = form.cleaned_data['blood_group']
        units = form.cleaned_data['units']
        action = form.cleaned_data['action']
        stock, _ = BloodStock.objects.get_or_create(blood_group=bg, defaults={'units_available': 0})
        if action == 'add':
            stock.units_available += units
        elif action == 'subtract':
            stock.units_available = max(0, stock.units_available - units)
        elif action == 'set':
            stock.units_available = units
        stock.save()
        messages.success(request, f'Blood stock for {bg} updated successfully.')
        return redirect('blood_stock')
    return render(request, 'hospital_admin_app/blood_stock.html', {'stocks': stocks, 'form': form})


@admin_required
def manage_users(request):
    role = request.GET.get('role', '')
    users = CustomUser.objects.exclude(role='hospital_admin').order_by('-created_at')
    if role:
        users = users.filter(role=role)
    return render(request, 'hospital_admin_app/manage_users.html', {
        'users': users,
        'current_role': role,
    })


@admin_required
def verify_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_verified = not user.is_verified
    user.save()
    status = 'verified' if user.is_verified else 'unverified'
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('manage_users')