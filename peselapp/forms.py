from django import forms

class PeselForm(forms.Form):
    """
    Django form for entering a pesel number.
    """
    pesel = forms.CharField(
        label="Numer PESEL",
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={
            "placeholder": "Wpisz 11 cyfr",
        }),
    )
