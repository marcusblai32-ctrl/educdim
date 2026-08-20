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
    
    # ===== NOUVEAU FIELD (Backward compatible) =====
    max_courses = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre maximum de cours",
        help_text="0 = tous les cours du plan (ancien comportement). Sinon, limite le nombre de cours que l'utilisateur peut choisir."
    )
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan d'abonnement"
        verbose_name_plural = "Plans d'abonnement"
        ordering = ['prix']

    def __str__(self):
        return f"{self.nom} - {self.prix} HTG"

    def get_courses_count(self):
        """Retounen kantite kou total nan plan an."""
        return self.cours.count()


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

    # ===== NOUVEAU FIELD (Backward compatible) =====
    courses_selectionnes = models.BooleanField(
        default=False,
        verbose_name="Cours sélectionnés",
        help_text="Indique si l'utilisateur a choisi ses cours (pour les plans avec max_courses > 0)."
    )

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

    # ===== NOUVEAU METÒD =====
    def get_courses_disponibles(self):
        """Retounen kou ki disponib pou seleksyon selon max_courses."""
        if self.plan.max_courses == 0:
            # Ansyen konpòtman: tout kou plan an
            return self.plan.cours.all()
        else:
            # Nouvo: kou plan an ki poko chwazi
            deja_chwazi = self.course_selections.values_list('course_id', flat=True)
            return self.plan.cours.exclude(id__in=deja_chwazi)

    def get_courses_deja_selectionnes(self):
        """Retounen kou deja seleksyone yo."""
        return self.course_selections.all()

    def get_places_restantes(self):
        """Retounen kantite plas ki rete pou chwazi kou."""
        if self.plan.max_courses == 0:
            return None
        deja_chwazi = self.course_selections.count()
        return max(0, self.plan.max_courses - deja_chwazi)

    def activer_avec_selection(self, courses_list):
        """Aktive abònman an epi kreye aksè pou kou seleksyone yo."""
        from django.db import transaction
        
        with transaction.atomic():
            # Kreye seleksyon kou yo
            for course in courses_list:
                SubscriptionCourseSelection.objects.get_or_create(
                    subscription=self,
                    course=course
                )
            
            # Kreye aksè pou kou seleksyone yo
            for course in courses_list:
                SubscriptionAccess.objects.get_or_create(
                    subscription=self,
                    cours=course,
                    defaults={'date_expiration': self.date_fin}
                )
            
            # Make kòm seleksyone
            self.courses_selectionnes = True
            self.save(update_fields=['courses_selectionnes'])


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


# ===== NOUVEAU MODEL =====
class SubscriptionCourseSelection(models.Model):
    """Seleksyon kou itilizatè a pou abònman li."""
    
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='course_selections',
        verbose_name="Abonnement"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscription_selections',
        verbose_name="Cours"
    )
    date_selection = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscription', 'course')
        verbose_name = "Sélection de cours"
        verbose_name_plural = "Sélections de cours"
        ordering = ['date_selection']

    def __str__(self):
        return f"{self.subscription.utilisateur.get_full_name()} - {self.course.titre}"