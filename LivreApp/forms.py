from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'isbn', 'date_publication', 'quantite', 'image', 'description', 'prix', 'disponible']
