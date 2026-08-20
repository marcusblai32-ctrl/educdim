from django.db import models
from django.conf import settings
from courses.models import Course
from django.utils import timezone

class SubscriptionPlan(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du plan")
    description = models.TextField(blank=True, verbose_name="Description")
    cours = models.ManyToManyField(Course, related_name='subscription_plans', verbose_name="Cours inclus")
    prix = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Prix")
    duree_jours = models.PositiveIntegerField(default=30, verbose_name="Durée (jours)")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan d'abonnement"
        verbose_name_plural = "Plans d'abonnement"
        ordering = ['prix']

    def __str__(self):
        return f"{self.nom} - {self.prix} HTG"

class Subscription(models.Model):
    METHODES_PAIEMENT = [
        ('moncash', 'MonCash'),
        ('natcash', 'NatCash'),
    ]

    STATUTS = [
        ('pending', 'En attente'),
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('cancelled', 'Annulé'),
        ('rejected', 'Refusé'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    statut = models.CharField(max_length=20, choices=STATUTS, default='pending')
    methode_paiement = models.CharField(max_length=15, choices=METHODES_PAIEMENT, default='moncash')

    nom_compte = models.CharField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    id_transaction = models.CharField(max_length=100, blank=True)
    photo_paiement = models.ImageField(upload_to='paiements/subscriptions/', blank=True, null=True)

    date_demande = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    date_verification = models.DateTimeField(null=True, blank=True)

    verifie_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions_verifiees')
    note_admin = models.TextField(blank=True)

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ['-date_demande']

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.plan.nom} ({self.get_statut_display()})"

    def est_actif(self):
        if self.statut != 'active':
            return False
        if self.date_fin and timezone.now() > self.date_fin:
            return False
        return True

    def jours_restants(self):
        if not self.date_fin:
            return 0
        delta = self.date_fin - timezone.now()
        return max(0, delta.days)

    def delete_photo(self):
        if self.photo_paiement:
            try:
                import os
                if os.path.isfile(self.photo_paiement.path):
                    os.remove(self.photo_paiement.path)
                self.photo_paiement = None
                self.save()
                return True
            except:
                pass
        return False

class SubscriptionAccess(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='accesses')
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription_accesses')
    date_acces = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('subscription', 'cours')
        verbose_name = "Accès par abonnement"
        verbose_name_plural = "Accès par abonnements"

    def __str__(self):
        return f"{self.subscription.utilisateur.get_full_name()} - {self.cours.titre}"
