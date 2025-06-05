from beartype import beartype
from django.core.management.base import BaseCommand
from authentication.tasks import cleanup_expired_sessions

class Command(BaseCommand):
    help = "Clean up expired user sessions."

    @beartype
    def handle(self, *args: object, **options: object) -> None:
        cleanup_expired_sessions()
        self.stdout.write(self.style.SUCCESS("Expired sessions cleanup complete."))
