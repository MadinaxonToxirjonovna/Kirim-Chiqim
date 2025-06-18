from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['rasm', 'manzil', 'telefon',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rasm'].required = False


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")
    telefon = forms.CharField(max_length=20, required=False, label="Telefon raqami")

    class Meta:
        model = User
        fields = ['username', 'telefon', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if not Profil.objects.filter(user=user).exists():
                Profil.objects.create(
                    user=user,
                    telefon=self.cleaned_data['telefon']
                )
        return user
