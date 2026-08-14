from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notifications.models import Notification
from courses.models import Lecon
from enrollments.models import Enrollment
from badges.models import BadgeUtilisateur
from quiz.models import TentativeQuiz
from progress.models import ProgresLecon

User = get_user_model()

@receiver(post_save, sender=Enrollment)
def notify_enrollment_status(sender, instance, created, **kwargs):
    if instance.statut == 'active' and not created:
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            type_notif='systeme',
            titre="Inscription approuvée",
            message=f"Votre inscription au cours '{instance.cours.titre}' a été approuvée.",
            lien=f"/cours/{instance.cours.pk}/"
        )
    elif instance.statut == 'rejected' and not created:
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            type_notif='systeme',
            titre="Inscription refusée",
            message=f"Votre inscription au cours '{instance.cours.titre}' a été refusée.",
            lien=f"/cours/{instance.cours.pk}/"
        )

@receiver(post_save, sender=Lecon)
def notify_new_lesson(sender, instance, created, **kwargs):
    if created:
        inscriptions = Enrollment.objects.filter(cours=instance.module.unite.cours, statut='active')
        for ins in inscriptions:
            Notification.objects.create(
                utilisateur=ins.utilisateur,
                type_notif='lecon',
                titre="Nouvelle leçon disponible",
                message=f"Une nouvelle leçon '{instance.titre}' est disponible dans votre cours.",
                lien=f"/cours/lecon/{instance.pk}/"
            )

@receiver(post_save, sender=TentativeQuiz)
def notify_quiz_result(sender, instance, created, **kwargs):
    if instance.date_soumission:
        if instance.reussi:
            msg = f"Bravo ! Vous avez réussi le quiz '{instance.quiz.titre}' avec {instance.score}%."
        else:
            msg = f"Vous avez échoué au quiz '{instance.quiz.titre}' avec {instance.score}%. Réessayez !"
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            type_notif='quiz',
            titre="Résultat de quiz",
            message=msg,
            lien=f"/quiz/resultat/{instance.pk}/"
        )

@receiver(post_save, sender=BadgeUtilisateur)
def notify_badge_earned(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            type_notif='badge',
            titre="Nouveau badge !",
            message=f"Vous avez obtenu le badge '{instance.badge.nom}'.",
            lien=f"/badges/detail/{instance.badge.pk}/"
        )

@receiver(post_save, sender=ProgresLecon)
def notify_lesson_complete(sender, instance, created, **kwargs):
    if instance.statut == 'termine' and not created:
        Notification.objects.create(
            utilisateur=instance.utilisateur,
            type_notif='lecon',
            titre="Leçon terminée",
            message=f"Félicitations ! Vous avez terminé la leçon '{instance.lecon.titre}'.",
            lien=f"/cours/lecon/{instance.lecon.pk}/"
        )
