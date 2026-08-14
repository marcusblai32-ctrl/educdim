from django.contrib import admin
from .models import SessionPresence, FichePresence, JustificationAbsence

class FichePresenceInline(admin.TabularInline):
    model = FichePresence
    extra = 0

@admin.register(SessionPresence)
class SessionPresenceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'date', 'heure_debut')
    inlines = [FichePresenceInline]

@admin.register(FichePresence)
class FichePresenceAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'session', 'statut')

@admin.register(JustificationAbsence)
class JustificationAbsenceAdmin(admin.ModelAdmin):
    list_display = ('fiche', 'date_soumission', 'examinee', 'approuvee')
