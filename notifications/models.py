from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = [
        ('lecon', 'Nouvelle leçon'),
        ('quiz', 'Quiz noté'),
        ('badge', 'Badge obtenu'),
        ('reunion', 'Réunion'),
        ('message', 'Message'),
        ('systeme', 'Système'),
    ]
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type_notif = models.CharField(max_length=15, choices=TYPES, verbose_name="Type")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    lien = models.URLField(blank=True, verbose_name="Lien")
    lue = models.BooleanField(default=False, verbose_name="Lue")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date']

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.titre}"
