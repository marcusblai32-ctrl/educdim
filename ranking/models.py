from django.db import models
from django.conf import settings

class Niveau(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du niveau")
    points_min = models.PositiveIntegerField(default=0, verbose_name="Points minimum")
    icone = models.ImageField(upload_to='niveaux/', blank=True, null=True, verbose_name="Icône")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre']

    def __str__(self):
        return self.nom

class PointsUtilisateur(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points_classement')
    total = models.PositiveIntegerField(default=0, verbose_name="Points totaux")
    semaine = models.PositiveIntegerField(default=0, verbose_name="Points cette semaine")
    mois = models.PositiveIntegerField(default=0, verbose_name="Points ce mois")
    derniere_maj = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Points de l'utilisateur"
        verbose_name_plural = "Points des utilisateurs"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.total} pts"

class HistoriquePoints(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historique_points')
    points = models.PositiveIntegerField(verbose_name="Points gagnés")
    raison = models.CharField(max_length=100, verbose_name="Raison")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique de points"
        verbose_name_plural = "Historiques de points"
        ordering = ['-date']

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} +{self.points} ({self.raison})"
