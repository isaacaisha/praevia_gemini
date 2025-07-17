# /home/siisi/praevia_gemini/praevia_api/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Action, Document, Contentieux, DossierATMP, Audit
)

# ───────────────────────────────
# Custom User Admin
# ───────────────────────────────
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)

# ───────────────────────────────
# Action Admin
# ───────────────────────────────
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

# ───────────────────────────────
# Document Admin
# ───────────────────────────────
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'document_type', 'uploaded_by', 'contentieux', 'created_at')
    list_filter = ('document_type',)
    search_fields = ('original_name', 'mime_type')
    ordering = ('-created_at',)

# ───────────────────────────────
# Contentieux Admin
# ───────────────────────────────
@admin.register(Contentieux)
class ContentieuxAdmin(admin.ModelAdmin):
    list_display = ('reference', 'dossier_atmp', 'status', 'created_at')
    search_fields = ('reference',)
    list_filter = ('status',)
    ordering = ('-created_at',)

# ───────────────────────────────
# DossierATMP Admin
# ───────────────────────────────
@admin.register(DossierATMP)
class DossierATMPAdmin(admin.ModelAdmin):
    list_display = ('reference', 'status', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('reference', 'created_by__email')
    ordering = ('-created_at',)

# ───────────────────────────────
# Audit Admin
# ───────────────────────────────
@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('dossier_atmp', 'auditor', 'status', 'decision', 'created_at')
    list_filter = ('status', 'decision')
    search_fields = ('dossier_atmp__reference', 'auditor__email')
    ordering = ('-created_at',)
