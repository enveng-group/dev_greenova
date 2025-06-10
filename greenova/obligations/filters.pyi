from _typeshed import Incomplete
from beartype import beartype
from django_filters import FilterSet

from .models import Obligation as Obligation

@beartype
def get_status_choices() -> list[tuple[str, str]]: ...

class ObligationFilter(FilterSet):
    obligation_number: Incomplete
    obligation: Incomplete
    status: Incomplete
    action_due_date: Incomplete
    recurring_obligation: Incomplete
    project_phase: Incomplete
    primary_environmental_mechanism: Incomplete
    class Meta:
        model = Obligation
        fields: Incomplete
