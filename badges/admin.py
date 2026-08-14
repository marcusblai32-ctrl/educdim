from django.contrib import admin
from .models import Badge, BadgeUtilisateur

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'condition_type', 'valeur_cible', 'actif')

@admin.register(BadgeUtilisateur)
class BadgeUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'badge', 'date_attribution')
