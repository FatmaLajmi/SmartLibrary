import base64
from django.db import models
from django.conf import settings
from django.utils.html import format_html


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bank_card_number = models.CharField(max_length=20, blank=True, null=True)
    image_blob = models.BinaryField(blank=True, null=True)  # 🔹 Nouveau champ

    def image_tag(self):
        """Display image preview in admin"""
        if self.image_blob:
            b64 = base64.b64encode(self.image_blob).decode()
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="60" height="60" '
                'style="object-fit: cover; border-radius:50%; border:2px solid #C5A992;" />',
                b64
            )
        return "—"
    image_tag.short_description = "Photo"

    def __str__(self):
        return self.user.email