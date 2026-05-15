from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileUpdateForm
from .models import CustomUser, BloodStock


def home(request):
    stocks = BloodStock.objects.all()
    total_donors = CustomUser.objects.filter(role='donor', is_verified=True).count()
    total_requesters = CustomUser.objects.filter(role='requester').count()
    return render(request, 'public_app/home.html', {
        'stocks': stocks,
        'total_donors': total_donors,
        'total_requesters': total_requesters,
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome {user.username}! Your account has been created.')
        return redirect_by_role(user)
    return render(request, 'public_app/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect_by_role(user)
    return render(request, 'public_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def redirect_by_role(user):
    if user.role == 'donor':
        return redirect('donor_dashboard')
    elif user.role == 'requester':
        return redirect('requester_dashboard')
    elif user.role == 'hospital_admin':
        return redirect('admin_dashboard')
    return redirect('home')


@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'public_app/profile.html', {'form': form})


def blood_availability(request):
    stocks = BloodStock.objects.all()
    return render(request, 'public_app/blood_availability.html', {'stocks': stocks})