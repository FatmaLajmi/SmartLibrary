from django.db import models
from LivreApp.models import Livre

class Avis(models.Model):
    book_id = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField()  # 0-5
    commentaire = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.book_id.title} - {self.note}/5"
    
    @property
    def book_title(self):
        return self.book_id.title
    
    @property
    def author(self):
        return self.book_id.author

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        ordering = ['-date']