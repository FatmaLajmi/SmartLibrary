from django.contrib import admin

from .models import Book, Avis

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('idAvis', 'book', 'user', 'note', 'date')
    list_filter = ('note', 'date')
    search_fields = ('commentaire', 'book__title', 'user__username')