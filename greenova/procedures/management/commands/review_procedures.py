from beartype import beartype
from django.core.management.base import BaseCommand
from procedures.tasks import review_procedures

class Command(BaseCommand):
    help = "Review procedures due for review and update their status/log actions."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        review_procedures()
        self.stdout.write(self.style.SUCCESS("Procedures review complete."))
