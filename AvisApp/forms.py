from django import forms
from .models import Avis

class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['book', 'note', 'commentaire']
        widgets = {
            'commentaire': forms.Textarea(attrs={'rows':4}),
        }

    def clean_note(self):
        note = self.cleaned_data.get('note')
        if note is None:
            raise forms.ValidationError("La note est requise.")
        if not (1 <= note <= 5):
            raise forms.ValidationError("La note doit être entre 1 et 5.")
        return note