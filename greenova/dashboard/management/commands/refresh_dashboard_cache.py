from beartype import beartype
from django.core.management.base import BaseCommand
from dashboard.tasks import refresh_dashboard_cache

class Command(BaseCommand):
    help = "Precompute and cache dashboard charts for all projects."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        refresh_dashboard_cache()
        self.stdout.write(self.style.SUCCESS("Dashboard cache refreshed."))
