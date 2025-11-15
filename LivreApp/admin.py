from django.contrib import admin
from .models import Livre


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'titre', 'auteur', 'isbn', 'quantite', 'disponible', 'date_ajout')
    list_display_links = ('image_tag', 'titre')  # clic direct
    
    # Formulaire admin
    fieldsets = (
        ("Informations principales", {
            'fields': ('titre', 'auteur', 'isbn', 'description', 'image')
        }),
        ("Détails supplémentaires", {
            'fields': ('date_publication', 'prix', 'quantite', 'disponible')
        }),
        ("Dates (auto)", {
            'fields': ('date_ajout', 'date_modif'),
            'classes': ('collapse',),  # réduit automatiquement
        }),
    )

    readonly_fields = ('date_ajout', 'date_modif', 'image_tag')

