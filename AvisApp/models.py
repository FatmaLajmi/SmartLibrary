from django.db import models

from django.db import models
from django.conf import settings

class Book(models.Model):
    # modèle minimal pour tester la gestion des avis
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Avis(models.Model):
    idAvis = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avis')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='avis')
    note = models.PositiveSmallIntegerField()  # on validera 1..5 dans le formulaire
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)   # date de création
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']  # par défaut les plus récents d'abord

    def __str__(self):
        return f"Avis {self.idAvis} - {self.book} - {self.user}"
