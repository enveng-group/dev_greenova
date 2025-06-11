from _typeshed import Incomplete
from django.core.management.base import BaseCommand

logger: Incomplete

class Command(BaseCommand):
    help: str
    def add_arguments(self, parser) -> None: ...
    def handle(self, *args, **options) -> None: ...
