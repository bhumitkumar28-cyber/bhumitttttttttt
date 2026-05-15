from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from public_app.models import BloodRequest, Notification, BloodStock
from .forms import BloodRequestForm


def requester_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'requester':
            messages.error(request, 'Access denied.')
            return redirect('login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@requester_required
def dashboard(request):
    requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    stats = {
        'total': requests.count(),
        'approved': requests.filter(status='approved').count(),
        'pending': requests.filter(status='pending').count(),
        'fulfilled': requests.filter(status='fulfilled').count(),
    }
    stocks = BloodStock.objects.all()
    return render(request, 'requester_app/dashboard.html', {
        'requests': requests[:5],
        'stats': stats,
        'notifications': notifications,
        'stocks': stocks,
    })


@requester_required
def request_blood(request):
    form = BloodRequestForm(request.POST or None, initial={'city': request.user.city})
    if request.method == 'POST' and form.is_valid():
        blood_req = form.save(commit=False)
        blood_req.requester = request.user
        blood_req.save()
        Notification.objects.create(
            user=request.user,
            title='Blood Request Submitted',
            message=f'Your request for {blood_req.units_needed} unit(s) of {blood_req.blood_group} blood has been submitted.'
        )
        messages.success(request, 'Blood request submitted successfully!')
        return redirect('requester_dashboard')
    return render(request, 'requester_app/request_blood.html', {'form': form})


@requester_required
def request_history(request):
    requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requester_app/request_history.html', {'requests': requests})


@requester_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('requester_dashboard')