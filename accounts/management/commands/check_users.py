from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Afiche tout itilizatè ak aktivite yo"

    def handle(self, *args, **options):
        users = CustomUser.objects.filter(is_staff=False)
        self.stdout.write("=" * 70)
        self.stdout.write(f"{'Email':<30} {'Dernière activité':<20} {'Inactif (jours)':<15} {'Statut':<15}")
        self.stdout.write("=" * 70)

        for user in users:
            delta = timezone.now() - user.last_activity
            days = delta.days
            if days > 90:
                status = "🔴 Inactif"
            elif days > 60:
                status = "🟡 Bientôt"
            else:
                status = "🟢 Actif"
            if user.notification_sent:
                status += " 📧"
            if user.delete_scheduled:
                status += " 🗑️"
            self.stdout.write(f"{user.email:<30} {user.last_activity.strftime('%d/%m/%Y'):<20} {days:<15} {status:<15}")
