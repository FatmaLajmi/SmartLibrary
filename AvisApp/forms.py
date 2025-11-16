# AvisApp/forms.py
from django import forms
from .models import Avis

class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['book_title','author','note','commentaire']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
        }

    def clean_note(self):
        n = self.cleaned_data.get('note')
        if n is None:
            raise forms.ValidationError("La note est requise")
        if n < 0 or n > 5:
            raise forms.ValidationError("La note doit être entre 0 et 5")
        return n
