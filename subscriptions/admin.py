from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import SubscriptionPlan, Subscription, SubscriptionAccess
from notifications.models import Notification

class SubscriptionAccessInline(admin.TabularInline):
    model = SubscriptionAccess
    extra = 0
    readonly_fields = ('date_acces', 'date_expiration')

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'duree_jours', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'description')
    filter_horizontal = ('cours',)
    fieldsets = (
        (None, {'fields': ('nom', 'description', 'prix', 'duree_jours', 'actif')}),
        ('Cours inclus', {'fields': ('cours',)}),
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'plan', 'statut', 'methode_paiement', 'date_demande', 'est_actif')
    list_filter = ('statut', 'methode_paiement', 'plan')
    search_fields = ('utilisateur__email', 'utilisateur__first_name', 'id_transaction')
    readonly_fields = ('date_demande',)
    inlines = [SubscriptionAccessInline]

    fieldsets = (
        ('Informations générales', {'fields': ('utilisateur', 'plan', 'statut', 'methode_paiement')}),
        ('Paiement', {'fields': ('nom_compte', 'telephone', 'id_transaction', 'photo_paiement')}),
        ('Dates', {'fields': ('date_demande', 'date_debut', 'date_fin', 'date_verification')}),
        ('Administration', {'fields': ('verifie_par', 'note_admin')}),
    )

    actions = ['approuver_paiement', 'rejeter_paiement']

    def approuver_paiement(self, request, queryset):
        count = 0
        for sub in queryset:
            if sub.statut == 'pending':
                sub.statut = 'active'
                sub.date_debut = timezone.now()
                sub.date_fin = timezone.now() + timezone.timedelta(days=sub.plan.duree_jours)
                sub.date_verification = timezone.now()
                sub.verifie_par = request.user
                sub.save()

                sub.delete_photo()

                for cours in sub.plan.cours.all():
                    SubscriptionAccess.objects.create(
                        subscription=sub,
                        cours=cours,
                        date_expiration=sub.date_fin
                    )

                Notification.objects.create(
                    utilisateur=sub.utilisateur,
                    type_notif='systeme',
                    titre="Abonnement approuvé",
                    message=f"Votre abonnement '{sub.plan.nom}' a été approuvé.",
                    lien="/abonnements/mes-abonnements/"
                )
                count += 1
        messages.success(request, f"{count} abonnements approuvés.")

    def rejeter_paiement(self, request, queryset):
        count = 0
        for sub in queryset:
            if sub.statut == 'pending':
                sub.statut = 'rejected'
                sub.date_verification = timezone.now()
                sub.verifie_par = request.user
                sub.save()

                sub.delete_photo()

                Notification.objects.create(
                    utilisateur=sub.utilisateur,
                    type_notif='systeme',
                    titre="Abonnement refusé",
                    message=f"Votre abonnement '{sub.plan.nom}' a été refusé.",
                    lien="/abonnements/mes-abonnements/"
                )
                count += 1
        messages.success(request, f"{count} abonnements rejetés.")
