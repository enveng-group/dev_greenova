from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from logging import getLogger
from .models import Project
from obligations.models import Obligation

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