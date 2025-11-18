from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Utilisateur

class ClientFilter(admin.SimpleListFilter):
    title = 'User Type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('client', 'Clients'),
            ('admin', 'Admins'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'client':
            return queryset.filter(role='client')
        if self.value() == 'admin':
            return queryset.filter(role='admin', is_superuser=False)
        return queryset

class UtilisateurAdmin(BaseUserAdmin):
    list_display = ('email', 'get_full_name', 'role', 'date_joined', 'is_active', 'role_badge')
    list_filter = (ClientFilter, 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'
    
    def role_badge(self, obj):
        if obj.is_superuser:
            color = '#dc3545'  # Red for superuser
            role_text = 'SUPERUSER'
        elif obj.role == 'admin':
            color = '#C5A992'  # Booksaw accent color for admin
            role_text = 'ADMIN'
        else:
            color = '#28a745'  # Green for client
            role_text = 'CLIENT'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color, role_text
        )
    role_badge.short_description = 'Status'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show all users for superuser, filter for regular admins if needed
        return qs
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Separate admin classes for filtering in admin site
class ClientAdmin(UtilisateurAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role='client')

class AdminUserAdmin(UtilisateurAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role='admin', is_superuser=False)

# Register the main model with all users
admin.site.register(Utilisateur, UtilisateurAdmin)

# Customize admin site headers
admin.site.site_header = "SmartLibrary Administration"
admin.site.site_title = "SmartLibrary Admin"
admin.site.index_title = "Welcome to SmartLibrary Admin Panel"

