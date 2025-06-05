from beartype import beartype
from django.core.management.base import BaseCommand
from responsibility.tasks import check_responsibility_compliance

class Command(BaseCommand):
    help = "Check for obligations missing responsibility assignments and log them."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        check_responsibility_compliance()
        self.stdout.write(self.style.SUCCESS("Responsibility compliance check complete."))
