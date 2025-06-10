from beartype import beartype
from django.core.management.base import BaseCommand
from obligations.tasks import send_obligation_reminders as send_obligation_reminders

class Command(BaseCommand):
    help: str
    @beartype
    def handle(self, *args: object, **options: object) -> None: ...
