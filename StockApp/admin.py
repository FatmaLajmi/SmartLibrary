from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'min_quantity', 'max_quantity', 'status')
    list_filter = ('status',)
    search_fields = ('book__titre', 'book__auteur', 'book__isbn')
    readonly_fields = ('status', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Book', {
            'fields': ('book',)
        }),
        ('Stock Levels', {
            'fields': ('quantity', 'min_quantity', 'max_quantity')
        }),
        ('Info', {
            'fields': ('status', 'created_at', 'updated_at'),
        }),
    )