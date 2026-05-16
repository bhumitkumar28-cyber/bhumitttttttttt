
from django.db import models
from django.contrib.auth.models import AbstractUser

BLOOD_GROUPS = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
                ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')]

ROLES = [('donor','Donor'),('requester','Requester'),('hospital_admin','Hospital Admin')]

STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('fulfilled','Fulfilled')]


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLES, default='donor')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS, unique=True)
    units_available = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group}: {self.units_available} units"


class Donation(models.Model):
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    units = models.IntegerField(default=1)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    donation_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Donation by {self.donor.username} - {self.blood_group}"


class BloodRequest(models.Model):
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)
    units_needed = models.IntegerField(default=1)
    patient_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    urgency = models.CharField(max_length=20, choices=[('normal','Normal'),('urgent','Urgent'),('critical','Critical')], default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    required_by = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.requester.username} - {self.blood_group}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"