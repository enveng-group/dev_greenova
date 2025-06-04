import django_tables2 as tables
from beartype import beartype

from .models import Obligation


@beartype
def get_obligation_table() -> type[tables.Table]:
    """Return a Table class for the Obligation model."""

    class ObligationTable(tables.Table):
        class Meta:
            model = Obligation
            template_name = "django_tables2/bootstrap4.html"
            fields = (
                "obligation_number",
                "project",
                "primary_environmental_mechanism",
                "procedure",
                "environmental_aspect",
                "status",
                "due_date",
            )

    return ObligationTable
