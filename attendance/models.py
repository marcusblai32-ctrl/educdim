from django.db import models
from django.conf import settings
from courses.models import Course

class SessionPresence(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions_presence', verbose_name="Cours")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    date = models.DateField(verbose_name="Date")
    heure_debut = models.TimeField(verbose_name="Heure début")
    heure_fin = models.TimeField(null=True, blank=True, verbose_name="Heure fin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Session de présence"
        verbose_name_plural = "Sessions de présence"
        ordering = ['-date', '-heure_debut']

    def __str__(self):
        return f"{self.cours.titre} - {self.titre} ({self.date})"

class FichePresence(models.Model):
    STATUTS = [
        ('present', 'Présent'),
        ('retard', 'En retard'),
        ('absent', 'Absent'),
        ('excuse', 'Excusé'),
    ]
    session = models.ForeignKey(SessionPresence, on_delete=models.CASCADE, related_name='fiches', verbose_name="Session")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fiches_presence', verbose_name="Utilisateur")
    statut = models.CharField(max_length=10, choices=STATUTS, default='absent', verbose_name="Statut")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        unique_together = ('session', 'utilisateur')
        verbose_name = "Fiche de présence"
        verbose_name_plural = "Fiches de présence"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.session} : {self.get_statut_display()}"

class JustificationAbsence(models.Model):
    fiche = models.OneToOneField(FichePresence, on_delete=models.CASCADE, related_name='justification', verbose_name="Fiche")
    raison = models.TextField(verbose_name="Raison")
    date_soumission = models.DateTimeField(auto_now_add=True)
    examinee = models.BooleanField(default=False, verbose_name="Examinée")
    approuvee = models.BooleanField(null=True, blank=True, verbose_name="Approuvée")
    note_admin = models.TextField(blank=True, verbose_name="Note admin")

    class Meta:
        verbose_name = "Justification d'absence"
        verbose_name_plural = "Justifications d'absence"

    def __str__(self):
        return f"Justification de {self.fiche.utilisateur.get_full_name()}"
