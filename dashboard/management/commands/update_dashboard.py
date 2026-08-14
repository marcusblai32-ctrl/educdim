from django.core.management.base import BaseCommand
from dashboard.models import AdminDashboard

class Command(BaseCommand):
    help = "Mete ajou dashboard admin"

    def handle(self, *args, **options):
        dashboard, created = AdminDashboard.objects.get_or_create(id=1)
        dashboard.update_stats()
        self.stdout.write(self.style.SUCCESS(f"✅ Dashboard mis à jour: {dashboard.last_updated}"))
