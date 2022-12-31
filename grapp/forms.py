from django import forms
from .models import Branch, Zone, HeadOffice


class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6, widget=forms.TextInput
                          (attrs={'class': 'form-control'}))


class loginform(forms.Form):
    Phone = forms.CharField(label="Phone", max_length=10, widget=forms.TextInput
                            (attrs={'class': 'form-control'}))


class HZBForm(forms.Form):

    ACCESS_LEVEL_CHOICES = [
        ("employee", "Employee"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    ]

    access_level = forms.ChoiceField(
        choices=ACCESS_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    head_office = forms.ModelChoiceField(
        queryset=HeadOffice.objects.all(),
        empty_label="-- Select a head office --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.all(),
        empty_label="-- Select a zone --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        empty_label="-- Select a branch --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
