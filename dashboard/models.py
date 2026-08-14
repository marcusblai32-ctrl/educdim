from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class AdminDashboard(models.Model):
    """Dashboard admin an tan reyèl"""
    total_users = models.PositiveIntegerField(default=0, verbose_name="Total utilisateurs")
    total_courses = models.PositiveIntegerField(default=0, verbose_name="Total cours")
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Revenu total")
    active_subscriptions = models.PositiveIntegerField(default=0, verbose_name="Abonnements actifs")

    # Estatistik kou
    total_lessons = models.PositiveIntegerField(default=0, verbose_name="Total leçons")
    total_quizzes = models.PositiveIntegerField(default=0, verbose_name="Total quiz")
    total_enrollments = models.PositiveIntegerField(default=0, verbose_name="Total inscriptions")

    # Estatistik itilizatè
    new_users_today = models.PositiveIntegerField(default=0, verbose_name="Nouveaux utilisateurs aujourd'hui")
    active_users_today = models.PositiveIntegerField(default=0, verbose_name="Utilisateurs actifs aujourd'hui")
    total_teachers = models.PositiveIntegerField(default=0, verbose_name="Total enseignants")

    # Revni
    revenue_this_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Revenu ce mois")
    revenue_this_week = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Revenu cette semaine")
    pending_payments = models.PositiveIntegerField(default=0, verbose_name="Paiements en attente")

    # Kwasans
    growth_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Croissance (%)")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        verbose_name = "Tableau de bord admin"
        verbose_name_plural = "Tableaux de bord admin"
        ordering = ['-last_updated']

    def __str__(self):
        return f"Dashboard - {self.last_updated.strftime('%d/%m/%Y %H:%M')}"

    def update_stats(self):
        """Mete ajou estatistik yo"""
        from accounts.models import CustomUser
        from courses.models import Course, Lecon
        from quiz.models import Quiz
        from enrollments.models import Enrollment
        from subscriptions.models import Subscription
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()
        start_of_today = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        start_of_week = timezone.now() - timedelta(days=7)
        start_of_month = timezone.now() - timedelta(days=30)

        # Mise à jour
        self.total_users = CustomUser.objects.filter(is_active=True).count()
        self.total_courses = Course.objects.filter(publie=True).count()
        self.total_lessons = Lecon.objects.filter(actif=True).count()
        self.total_quizzes = Quiz.objects.filter(publie=True).count()
        self.total_enrollments = Enrollment.objects.filter(statut='active').count()
        self.active_subscriptions = Subscription.objects.filter(statut='active').count()
        self.total_teachers = CustomUser.objects.filter(is_staff=True).count()

        # Nouveaux utilisateurs
        self.new_users_today = CustomUser.objects.filter(date_joined__gte=start_of_today).count()
        self.active_users_today = CustomUser.objects.filter(last_activity__gte=start_of_today).count()

        # Revenus (estimés)
        from enrollments.models import Enrollment
        total = Enrollment.objects.filter(statut='active').aggregate(Sum('cours__prix'))['cours__prix__sum'] or 0
        self.total_revenue = Decimal(str(total))

        # Revenu ce mois
        month_revenue = Enrollment.objects.filter(
            statut='active',
            date_demande__gte=start_of_month
        ).aggregate(Sum('cours__prix'))['cours__prix__sum'] or 0
        self.revenue_this_month = Decimal(str(month_revenue))

        # Revenu cette semaine
        week_revenue = Enrollment.objects.filter(
            statut='active',
            date_demande__gte=start_of_week
        ).aggregate(Sum('cours__prix'))['cours__prix__sum'] or 0
        self.revenue_this_week = Decimal(str(week_revenue))

        # Paiements en attente
        self.pending_payments = Enrollment.objects.filter(statut='pending').count()

        # Croissance
        last_month = timezone.now() - timedelta(days=60)
        last_month_users = CustomUser.objects.filter(date_joined__gte=last_month, date_joined__lt=start_of_month).count()
        if last_month_users > 0:
            growth = ((self.new_users_today - last_month_users) / last_month_users) * 100
            self.growth_percentage = Decimal(str(growth))
        else:
            self.growth_percentage = Decimal('0.00')

        self.save()
        return self
