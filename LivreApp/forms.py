from django import forms
from .models import Livre
from PIL import Image
import io

class LivreForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label="Image")

    class Meta:
        model = Livre
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get('image_upload')

        if file:
            # Charger l'image
            img = Image.open(file)

            # Convertir si pas en RGB
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Redimensionner à 220x318
            img = img.resize((220, 318), Image.Resampling.LANCZOS)

            # Réencoder l’image en JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")

            # Stocker dans le blob
            instance.image_blob = buffer.getvalue()

        if commit:
            instance.save()
        return instance


