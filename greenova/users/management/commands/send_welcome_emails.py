from beartype import beartype
from django.core.management.base import BaseCommand
from users.tasks import send_welcome_emails

class Command(BaseCommand):
    help = "Send welcome emails to new users who have not received one."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        send_welcome_emails()
        self.stdout.write(self.style.SUCCESS("Welcome emails sent."))
