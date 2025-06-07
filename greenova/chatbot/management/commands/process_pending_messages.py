from beartype import beartype
from chatbot.tasks import process_pending_messages
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Process pending chat messages and mark them as sent."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        process_pending_messages()
        self.stdout.write(self.style.SUCCESS("Pending chat messages processed."))
