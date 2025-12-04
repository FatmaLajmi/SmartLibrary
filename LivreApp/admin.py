from django.contrib import admin
from .models import Livre
from .forms import LivreForm


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    form = LivreForm

    list_display = ('image_tag', 'title', 'author', 'isbn', 'genre', 'quantity', 'available', 'date_added')
    list_display_links = ('image_tag', 'title')

    #  Recherche (Admin) → SearchFields
    search_fields = ('title', 'author', 'isbn', 'genre', 'description')

    #  Filtres (Admin) → ListFilter
    list_filter = ('genre', 'available', 'date_added')
    
    # Admin form
    fieldsets = (
        ("Main Information", {
            'fields': ('title', 'author', 'isbn', 'genre', 'description', 'image_upload')  # ← Ajouter genre ici
        }),
        ("Additional Details", {
            'fields': ('publication_date', 'price', 'quantity', 'available')
        }),
        ("Automatic Dates", {
            'fields': ('date_added', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('date_added', 'date_modified', 'image_tag')
