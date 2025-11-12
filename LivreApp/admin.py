from django.contrib import admin
from .models import Livre

# Register your models here.

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'isbn', 'quantite', 'disponible', 'date_ajout')
    search_fields = ('titre', 'auteur', 'isbn')
    list_filter = ('disponible',)
