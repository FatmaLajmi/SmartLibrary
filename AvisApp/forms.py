# AvisApp/forms.py
from django import forms
from .models import Avis

class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 5,
                'placeholder': 'Entrez une note entre 0 et 5'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Partagez votre opinion sur ce livre...'
            }),
        }
        labels = {
            'note': 'Note (0-5)',
            'commentaire': 'Votre commentaire',
        }
        help_texts = {
            'note': 'Donnez une note entre 0 et 5 étoiles',
            'commentaire': 'Écrivez votre avis sur ce livre',
        }

    def clean_note(self):
        n = self.cleaned_data.get('note')
        if n is None:
            raise forms.ValidationError("La note est requise")
        if n < 0 or n > 5:
            raise forms.ValidationError("La note doit être entre 0 et 5")
        return n