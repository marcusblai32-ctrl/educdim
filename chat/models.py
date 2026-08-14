from django.db import models
from django.conf import settings
from courses.models import Course

class ChatRoom(models.Model):
    TYPES = [
        ('private', 'Prive'),
        ('group', 'Groupe'),
        ('feedback', 'Feedback'),
    ]
    nom = models.CharField(max_length=100, blank=True, verbose_name="Nom du salon")
    type = models.CharField(max_length=10, choices=TYPES, verbose_name="Type")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cours associe")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms', verbose_name="Participants")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_rooms', verbose_name="Cree par")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Salon de chat"
        verbose_name_plural = "Salons de chat"

    def __str__(self):
        return self.nom or f"{self.get_type_display()} - {self.id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', verbose_name="Salon")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    contenu = models.TextField(verbose_name="Contenu")
    reponse_a = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reponses', verbose_name="Reponse a")
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, verbose_name="Supprime")

    class Meta:
        ordering = ['created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.user.get_full_name()}: {self.contenu[:30]}"
