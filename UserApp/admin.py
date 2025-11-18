from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur
from django.forms import TextInput, Textarea
from django import forms

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'role', 'password')

class CustomUserAdmin(UserAdmin):
    model = Utilisateur
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'role', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Utilisateur, CustomUserAdmin)
