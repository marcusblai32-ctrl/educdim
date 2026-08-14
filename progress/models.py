from django.db import models
from django.conf import settings
from courses.models import Lecon, Course

class ProgresLecon(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progres_lecons')
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[
        ('non_commence', 'Non commencée'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminée'),
    ], default='non_commence')
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('utilisateur', 'lecon')
        verbose_name = "Progrès de leçon"
        verbose_name_plural = "Progrès des leçons"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.lecon.titre}"

class ProgresCours(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progres_cours')
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('utilisateur', 'cours')
        verbose_name = "Progrès de cours"
        verbose_name_plural = "Progrès des cours"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.cours.titre} : {self.pourcentage}%"
