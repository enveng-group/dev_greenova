"""FilterSet classes for obligations app using django-filter.

This module defines reusable filters for the Obligation model.
"""

from beartype import beartype
from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
)

from .models import Obligation


@beartype
def get_status_choices() -> list[tuple[str, str]]:
    """Return status choices for filtering."""
    return Obligation._meta.get_field("status").choices


@beartype
class ObligationFilter(FilterSet):
    """FilterSet for the Obligation model."""

    obligation_number = CharFilter(lookup_expr="icontains", label="Obligation Number")
    obligation = CharFilter(lookup_expr="icontains", label="Obligation Text")
    status = ChoiceFilter(choices=get_status_choices, label="Status")
    action_due_date = DateFilter(
        field_name="action_due_date",
        lookup_expr="exact",
        label="Due Date",
    )
    recurring_obligation = BooleanFilter(label="Recurring")
    project_phase = CharFilter(lookup_expr="icontains", label="Project Phase")
    primary_environmental_mechanism = CharFilter(
        field_name="primary_environmental_mechanism__name",
        lookup_expr="icontains",
        label="Mechanism",
    )

    class Meta:
        model = Obligation
        fields = [
            "obligation_number",
            "obligation",
            "status",
            "action_due_date",
            "recurring_obligation",
            "project_phase",
            "primary_environmental_mechanism",
        ]
