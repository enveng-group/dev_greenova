from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from logging import getLogger
from .models import Project, Obligation

logger = getLogger(__name__)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""
    list_display = ('id', 'name')
    search_fields = ('name',)

    def save_model(self, request: HttpRequest, obj: Project, form: ModelForm, change: bool) -> None:
        try:
            logger.info(f"Admin saving project: {obj.name}")
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Admin save error: {str(e)}")
            raise

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    """Admin configuration for analytics views of obligations."""
    list_display = (
        'obligation_number',
        'primary_environmental_mechanism', 
        'status',
        'action_due_date'
    )
    list_filter = (
        'status',
        'primary_environmental_mechanism',
        'environmental_aspect'
    )
    search_fields = (
        'obligation_number',
        'primary_environmental_mechanism',
        'environmental_aspect'
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]:
        """Optimize queryset for admin view."""
        return super().get_queryset(request).select_related('project')