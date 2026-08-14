from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titre', 'placement', 'actif', 'ordre')
    list_filter = ('placement', 'actif')
    fieldsets = (
        (None, {'fields': ('titre', 'image', 'lien', 'ordre', 'actif', 'placement', 'largeur', 'hauteur')}),
    )
