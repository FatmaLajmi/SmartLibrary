from django.db import models
#from django.contrib.auth.models import User
#from SmartLibrary.LivreApp.models import Livre

class Panier(models.Model):
    """ 
    utilisateur = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE) 
    """
    titre = models.CharField(max_length=200)
    quantite = models.PositiveIntegerField(default=1)
    prix = models.DecimalField(max_digits=6, decimal_places=2)

    def prix_total(self):
        return self.quantite * self.prix

    def __str__(self):
        return f"{self.titre} ({self.quantite})"