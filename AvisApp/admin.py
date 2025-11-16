from django.contrib import admin
from .models import Avis

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'author', 'note', 'date')
    list_filter = ('date', 'note', 'book_title')
    search_fields = ('author', 'book_title', 'commentaire')