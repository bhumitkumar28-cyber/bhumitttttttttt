from django import forms
from public_app.models import BloodRequest


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_needed', 'patient_name', 'hospital_name', 'city', 'urgency', 'required_by', 'notes']
        widgets = {
            'required_by': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['required_by', 'notes']:
                field.widget.attrs['class'] = 'form-control'