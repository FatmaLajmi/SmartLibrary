from django import forms
from .models import Panier

class PanierForm(forms.ModelForm):
    class Meta:
        model = Panier
        fields = ['titre', 'quantite', 'prix']