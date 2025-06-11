from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help: str
    def handle(self, *args, **options) -> None: ...
