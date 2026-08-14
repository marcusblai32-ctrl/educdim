from django.contrib import admin
from .models import Niveau, PointsUtilisateur

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom', 'points_min', 'ordre')

@admin.register(PointsUtilisateur)
class PointsUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'total', 'semaine', 'mois')
