from django.db import models


# Create your models here.

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='livres/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_ajout']
        unique_together = (('titre', 'auteur', 'isbn'),)  # isbn unique, sinon combination allowed

    def __str__(self):
        return f"{self.titre} — {self.auteur}"
