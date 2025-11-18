from django.contrib import admin
from .models import Livre
from .forms import LivreForm


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    form = LivreForm

    list_display = ('image_tag', 'title', 'author', 'isbn', 'quantity', 'available', 'date_added')
    list_display_links = ('image_tag', 'title')
    
    # Admin form
    fieldsets = (
        ("Main Information", {
            'fields': ('title', 'author', 'isbn', 'description', 'image_upload')  # image → image_upload
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
