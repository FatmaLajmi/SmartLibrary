from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class UtilisateurRegisterForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ["first_name", "last_name", "email", "password1", "password2"]

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }
