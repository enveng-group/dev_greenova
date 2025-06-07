from beartype import beartype
from django.core.management.base import BaseCommand
from feedback.tasks import process_feedback_queue


class Command(BaseCommand):
    help = "Process unhandled feedback and mark as handled."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        process_feedback_queue()
        self.stdout.write(self.style.SUCCESS("Feedback queue processed."))
