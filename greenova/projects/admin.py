from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Project, Obligation

@admin.register(Project)
class ProjectAdmin(ModelAdmin[Project]):
    """Admin configuration for Project model.
    
    This class configures the admin interface for managing Project objects.
    Supports searching by name and displays ID and name columns.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Obligation)
class ObligationAdmin(ModelAdmin[Obligation]):
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