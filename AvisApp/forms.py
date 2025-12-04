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
                'placeholder': 'Enter a rating between 0 and 5'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your opinion about this book...'
            }),
        }
        labels = {
            'note': 'Rating (0-5)',
            'commentaire': 'Your comment',
        }
        help_texts = {
            'note': 'Give a rating between 0 and 5 stars',
            'commentaire': 'Write your review about this book',
        }

    def clean_note(self):
        n = self.cleaned_data.get('note')
        if n is None:
            raise forms.ValidationError("Rating is required")
        if n < 0 or n > 5:
            raise forms.ValidationError("Rating must be between 0 and 5")
        return n
