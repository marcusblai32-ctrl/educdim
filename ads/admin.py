from django.contrib import admin
from django.utils.html import format_html
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titre', 'placement', 'actif', 'ordre', 'preview_image')
    list_filter = ('placement', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)
    fieldsets = (
        (None, {'fields': ('titre', 'image', 'lien', 'ordre', 'actif', 'placement', 'largeur', 'hauteur')}),
    )
    
    def preview_image(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="max-height:50px; max-width:100px; border-radius:4px;" />', obj.image.url)
        return "-"
    preview_image.short_description = "Aperçu"