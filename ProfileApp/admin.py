from django.contrib import admin
from .models import Profile
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm

    list_display = ('image_tag', 'user', 'phone_number', 'address')
    list_display_links = ('image_tag', 'user')
    
    fieldsets = (
        ("Utilisateur", {
            'fields': ('user',)
        }),
        ("Informations personnelles", {
            'fields': ('address', 'phone_number', 'bank_card_number', 'image_upload')  # 🔹 image_upload
        }),
    )

    readonly_fields = ('image_tag',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')