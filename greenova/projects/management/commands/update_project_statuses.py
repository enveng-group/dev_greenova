from beartype import beartype
from django.core.management.base import BaseCommand
from projects.tasks import update_project_statuses


class Command(BaseCommand):
    help = "Check for inactive projects and log them."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        update_project_statuses()
        self.stdout.write(self.style.SUCCESS("Project status update complete."))
