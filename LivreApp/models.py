import base64
from django.db import models


# Create your models here.

from django.db import models
from django.utils.html import format_html


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)
    image_blob = models.BinaryField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.image_blob:
            b64 = base64.b64encode(self.image_blob).decode()
            return format_html(
                '<img src="data:image/jpeg;base64,{}" width="60" height="80" style="object-fit: cover; border-radius:4px;" />',
                b64
            )
        return "—"
    image_tag.short_description = "Aperçu"


    def __str__(self):
        return f"{self.titre} — {self.auteur}"

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        constraints = [
            models.UniqueConstraint(
                fields=['titre', 'auteur', 'isbn'],
                name='unique_livre_combinaison'
            )
        ]
