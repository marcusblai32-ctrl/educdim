from django.db import models
from django.conf import settings

class Badge(models.Model):
    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom du badge")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='badges/', blank=True, null=True, verbose_name="Image")
    condition_type = models.CharField(max_length=30, choices=[
        ('progression_cours', 'Progression dans un cours'),
        ('score_quiz', 'Score à un quiz'),
        ('presence', 'Taux de présence'),
        ('lecons_terminees', 'Nombre de leçons terminées'),
        ('manuel', 'Attribution manuelle'),
    ], default='manuel', verbose_name="Type de condition")
    valeur_cible = models.FloatField(null=True, blank=True, verbose_name="Valeur cible")
    cours = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cours concerné")
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Quiz concerné")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class BadgeUtilisateur(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_attribution = models.DateTimeField(auto_now_add=True)
    attribue_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges_attribues')

    class Meta:
        unique_together = ('utilisateur', 'badge')
        verbose_name = "Badge de l'utilisateur"
        verbose_name_plural = "Badges des utilisateurs"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.badge.nom}"
