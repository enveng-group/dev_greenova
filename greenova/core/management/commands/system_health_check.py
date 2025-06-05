from beartype import beartype
from django.core.management.base import BaseCommand
from core.tasks import system_health_check

class Command(BaseCommand):
    help = "Check system health and log status."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        system_health_check()
        self.stdout.write(self.style.SUCCESS("System health check complete."))
