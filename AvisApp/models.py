from django.db import models

class Avis(models.Model):
    # id automatique (id) fourni par Django
    note = models.IntegerField()  # 0-5 (contrainte possible)
    commentaire = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)  # date de création par défaut
    author = models.CharField(max_length=150, default="Inconnu")  # pour tester: le nom de l'user (remplacer plus tard par FK User)
    book_title = models.CharField(max_length=255, default="Inconnu")  # pour tester: titre du livre (remplacer par FK Book)

    def __str__(self):
        return f"{self.book_title} - {self.author} - {self.note}"