from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from .models import Obligation
import logging

logger = logging.getLogger(__name__)

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    """Admin configuration for obligations."""
    list_display = [
        'obligation_number',
        'project',
        'primary_environmental_mechanism',
        'status',
        'action_due_date'
    ]
    list_filter = [
        'status',
        'primary_environmental_mechanism',
        'project_phase',
        'recurring_obligation'
    ]
    search_fields = ['obligation_number', 'obligation', 'project__name']
    date_hierarchy = 'action_due_date'

    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]:
        """
        Optimize queryset for admin view by pre-fetching related fields.

        Args:
            request: The HTTP request object

        Returns:
            QuerySet: Optimized queryset with related fields
        """
        qs = super().get_queryset(request)
        return qs.select_related('project', 'primary_environmental_mechanism')

    def save_model(
            self,
            request: HttpRequest,
            obj: Obligation,
            form: ModelForm,
            change: bool) -> None:
        """
        Log obligation changes in admin.

        Args:
            request: The HTTP request object
            obj: The obligation instance being saved
            form: The model form instance
            change: Boolean indicating if this is an update
        """
        try:
            action = "Updated" if change else "Created"
            logger.info(
                f"{action} obligation {obj.obligation_number} "
                f"for project {obj.project.name}"
            )
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Error saving obligation: {str(e)}")
            raise
