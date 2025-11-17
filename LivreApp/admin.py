from django.contrib import admin
from .models import Livre
from .forms import LivreForm


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    form = LivreForm

    list_display = ('image_tag', 'titre', 'auteur', 'isbn', 'quantite', 'disponible', 'date_ajout')
    list_display_links = ('image_tag', 'titre')
    
    # Formulaire admin
    fieldsets = (
        ("Informations principales", {
            'fields': ('titre', 'auteur', 'isbn', 'description', 'image_upload')  # <--- changer image en image_upload
        }),
        ("Détails supplémentaires", {
            'fields': ('date_publication', 'prix', 'quantite', 'disponible')
        }),
        ("Dates (auto)", {
            'fields': ('date_ajout', 'date_modif'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('date_ajout', 'date_modif', 'image_tag')


