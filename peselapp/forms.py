from django import forms
from django.core.validators import RegexValidator

class PeselForm(forms.Form):
    pesel = forms.CharField(
        label="Numer PESEL",
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={
            "placeholder": "Wpisz 11 cyfr",
        }),
    )
