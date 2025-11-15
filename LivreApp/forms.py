from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label="Image")

    class Meta:
        model = Livre
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('image_upload')
        if file:
            instance.image_blob = file.read()  # convertit en BLOB
        if commit:
            instance.save()
        return instance
