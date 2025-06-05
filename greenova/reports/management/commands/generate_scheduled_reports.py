from beartype import beartype
from django.core.management.base import BaseCommand
from reports.tasks import generate_scheduled_reports

class Command(BaseCommand):
    help = "Generate a summary report for all reports created in the last 7 days."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        generate_scheduled_reports()
        self.stdout.write(self.style.SUCCESS("Scheduled reports generated."))
