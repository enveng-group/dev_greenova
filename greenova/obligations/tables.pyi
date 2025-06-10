import django_tables2 as tables
from beartype import beartype

from .models import Obligation as Obligation

@beartype
def get_obligation_table() -> type[tables.Table]: ...
