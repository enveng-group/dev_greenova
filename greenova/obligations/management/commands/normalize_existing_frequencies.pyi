from _typeshed import Incomplete
from django.core.management.base import BaseCommand
from obligations.models import Obligation as Obligation
from obligations.utils import normalize_frequency as normalize_frequency

logger: Incomplete

class Command(BaseCommand):
    help: str
    def add_arguments(self, parser) -> None: ...
    def handle(self, *args, **options) -> None: ...
