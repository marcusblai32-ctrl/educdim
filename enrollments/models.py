from django.db import models
from django.conf import settings
from courses.models import Course

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('active', 'Actif'),
        ('rejected', 'Refusé'),
        ('cancelled', 'Annulé'),
    ]
    METHODES_PAIEMENT = [
        ('moncash', 'MonCash'),
        ('natcash', 'NatCash'),
        ('manual', 'Attribution manuelle (admin)'),
        ('subscription', 'Abonnement'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscriptions', verbose_name="Utilisateur")
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='inscriptions', verbose_name="Cours")
    statut = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    methode_paiement = models.CharField(max_length=15, choices=METHODES_PAIEMENT, default='moncash', verbose_name="Méthode de paiement")
    nom_compte = models.CharField(max_length=200, blank=True, verbose_name="Nom sur le compte")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    id_transaction = models.CharField(max_length=100, blank=True, verbose_name="ID de transaction")
    photo_paiement = models.ImageField(upload_to='paiements/enrollments/', blank=True, null=True, verbose_name="Photo paiement")
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    verifie_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='inscriptions_verifiees', verbose_name="Vérifié par")
    date_verification = models.DateTimeField(null=True, blank=True, verbose_name="Date de vérification")
    note_admin = models.TextField(blank=True, verbose_name="Note admin")

    class Meta:
        unique_together = ('utilisateur', 'cours')
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        ordering = ['-date_demande']

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.cours.titre} ({self.get_statut_display()})"

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
