from django import forms
from public_app.models import Donation, BLOOD_GROUPS


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['blood_group', 'units', 'city', 'donation_date', 'notes']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['donation_date', 'notes']:
                field.widget.attrs['class'] = 'form-control'