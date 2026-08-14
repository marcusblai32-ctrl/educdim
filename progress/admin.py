from django.contrib import admin
from .models import ProgresLecon, ProgresCours

@admin.register(ProgresLecon)
class ProgresLeconAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'lecon', 'statut')

@admin.register(ProgresCours)
class ProgresCoursAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'cours', 'pourcentage')
