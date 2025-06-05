from beartype import beartype
from django.core.management.base import BaseCommand
from obligations.tasks import send_obligation_reminders

class Command(BaseCommand):
    help = "Send reminders for upcoming and overdue obligations."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        send_obligation_reminders()
        self.stdout.write(self.style.SUCCESS("Obligation reminders sent."))
