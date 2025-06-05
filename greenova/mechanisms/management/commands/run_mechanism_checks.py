from beartype import beartype
from django.core.management.base import BaseCommand
from mechanisms.tasks import run_mechanism_checks

class Command(BaseCommand):
    help = "Check for mechanisms with no or overdue obligations and log them."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        run_mechanism_checks()
        self.stdout.write(self.style.SUCCESS("Mechanism checks complete."))
