from django.contrib import admin, messages
from django.utils.html import format_html
from django.http import HttpResponse
from django.urls import path, reverse
from django.conf import settings
from django.core.mail import send_mail
import logging

from .models import Stock

logger = logging.getLogger(__name__)

# try to import export helpers; if missing, we will disable export actions gracefully
EXPORTS_AVAILABLE = True
try:
    from .export import export_stocks_to_excel, export_stocks_to_pdf
except Exception as e:
    EXPORTS_AVAILABLE = False
    logger.warning("Export helpers not available: %s", e)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # Use callable names (not 'book__title' strings)
    list_display = ('book__title', 'book__genre', 'quantity', 'min_quantity', 'max_quantity', 'status', 'low_stock_badge', 'stats_link')
    ordering = ('book__title',)
    list_filter = ('book__genre', 'book__author', 'status',)
    search_fields = ('book__title', 'book__author', 'book__isbn', 'book__genre')
    readonly_fields = ('status', 'created_at', 'updated_at')

    # Show custom change_list template (keeps your iframe/chart)
    change_list_template = "admin/StockApp/stock/change_list.html"

    # Register actions only if export helpers are present
    actions = ['export_as_excel', 'export_as_pdf'] if EXPORTS_AVAILABLE else []

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

    # helper display methods
    def book_title(self, obj):
        return getattr(obj.book, 'title', '')
    book_title.short_description = 'Book title'

    def book_category(self, obj):
        return getattr(obj.book, 'genre', '')
    book_category.short_description = 'Genre'

    def stats_link(self, obj):
        try:
            url = reverse('StockApp:stock_stats')
        except Exception:
            # fallback if no namespaced url
            try:
                url = reverse('stock_stats')
            except Exception:
                url = '#'
        return format_html('<a href="{}" target="_blank">View Stats</a>', url)
    stats_link.short_description = "Stats Page"

    def low_stock_badge(self, obj):
        try:
            qty = obj.quantity
            minq = obj.min_quantity if obj.min_quantity is not None else 0
        except Exception:
            return ''
        if qty <= 0:
            return format_html('<span style="color:#fff;background:#c62828;padding:2px 6px;border-radius:4px">Out</span>')
        if qty <= minq:
            return format_html('<span style="color:#fff;background:#ff7043;padding:2px 6px;border-radius:4px">Low</span>')
        return format_html('<span style="color:#fff;background:#4caf50;padding:2px 6px;border-radius:4px">OK</span>')
    low_stock_badge.short_description = 'Stock'

    # Admin actions (export selected)
    def export_as_excel(self, request, queryset):
        if not EXPORTS_AVAILABLE:
            self.message_user(request, "Export unavailable: missing export dependencies.", level=messages.ERROR)
            return
        if not queryset.exists():
            self.message_user(request, "Sélection vide.", level=messages.WARNING)
            return
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=stock_export.xlsx'
        export_stocks_to_excel(queryset, response)
        return response
    export_as_excel.short_description = "Exporter la sélection en Excel"

    def export_as_pdf(self, request, queryset):
        if not EXPORTS_AVAILABLE:
            self.message_user(request, "Export unavailable: missing export dependencies.", level=messages.ERROR)
            return
        if not queryset.exists():
            self.message_user(request, "Sélection vide.", level=messages.WARNING)
            return
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=stock_export.pdf'
        export_stocks_to_pdf(queryset, response)
        return response
    export_as_pdf.short_description = "Exporter la sélection en PDF"

    # Add custom admin URLs for exporting the current (filtered) changelist
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/all-excel/', self.admin_site.admin_view(self.export_all_excel), name='stock_export_all_excel'),
            path('export/all-pdf/', self.admin_site.admin_view(self.export_all_pdf), name='stock_export_all_pdf'),
        ]
        return custom_urls + urls

    def export_all_excel(self, request):
        qs = self.get_queryset(request)
        if not qs.exists():
            self.message_user(request, "Aucun élément à exporter.", level=messages.WARNING)
            return HttpResponse("No data to export", status=204)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=stock_export_all.xlsx'
        export_stocks_to_excel(qs, response)
        return response

    def export_all_pdf(self, request):
        qs = self.get_queryset(request)
        if not qs.exists():
            self.message_user(request, "Aucun élément à exporter.", level=messages.WARNING)
            return HttpResponse("No data to export", status=204)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=stock_export_all.pdf'
        export_stocks_to_pdf(qs, response)
        return response

    # Override save_model to notify when stock crosses below min_quantity
    def save_model(self, request, obj, form, change):
        old_qty = None
        if change and obj.pk:
            try:
                old = Stock.objects.get(pk=obj.pk)
                old_qty = old.quantity
            except Stock.DoesNotExist:
                old_qty = None

        super().save_model(request, obj, form, change)

        try:
            new_qty = obj.quantity
            min_q = obj.min_quantity if obj.min_quantity is not None else 0
            crossed = False
            if old_qty is None:
                if new_qty <= min_q:
                    crossed = True
            else:
                if old_qty > min_q and new_qty <= min_q:
                    crossed = True
        except Exception:
            crossed = False

        if crossed:
            self.message_user(request,
                f"Attention: le stock de « {obj.book.title} » est bas ({obj.quantity}).",
                level=messages.WARNING
            )
            # Optional email to ADMINS
            try:
                if getattr(settings, 'ADMINS', None):
                    subject = f"[Stock] Bas niveau: {obj.book.title}"
                    body = f"Le stock de '{obj.book.title}' ({obj.book.genre}) est à {obj.quantity}, seuil={obj.min_quantity}."
                    recipients = [a[1] for a in settings.ADMINS]
                    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)
            except Exception:
                pass