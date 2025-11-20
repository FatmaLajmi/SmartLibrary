from django import forms
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label="Photo de profil")  # 🔹 Champ pour upload

    class Meta:
        model = Profile
        fields = ['address', 'phone_number', 'bank_card_number']  # 🔹 Pas image_blob

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('image_upload')
        if file:
            instance.image_blob = file.read()  # 🔹 Convertir en BLOB
        if commit:
            instance.save()
        return instance


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']