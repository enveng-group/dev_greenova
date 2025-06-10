from _typeshed import Incomplete
from django.core.management.base import BaseCommand
from obligations.models import Obligation as Obligation

logger: Incomplete

class Command(BaseCommand):
    help: str
    def handle(self, *args, **options) -> None: ...
