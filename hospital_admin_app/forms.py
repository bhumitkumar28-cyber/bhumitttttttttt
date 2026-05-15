from django import forms
from public_app.models import BloodStock, BLOOD_GROUPS


class BloodStockForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = ['blood_group', 'units_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StockUpdateForm(forms.Form):
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS)
    units = forms.IntegerField(min_value=1)
    action = forms.ChoiceField(choices=[('add', 'Add'), ('subtract', 'Subtract'), ('set', 'Set')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'