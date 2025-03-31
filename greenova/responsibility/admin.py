from core.utils.roles import get_responsibility_choices
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import Responsibility


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for Responsibility model."""
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make name field readonly after creation to maintain referential integrity"""
        if obj:  # If editing existing object
            return ('name',)
        return ()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of responsibility values to maintain referential integrity"""
        # Only allow deletion if the responsibility is not used by any obligations
        if obj:
            # Check if this responsibility is being used by any obligations
            from obligations.models import Obligation
            if Obligation.objects.filter(responsibility=obj.name).exists():
                return False
        return True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-from-roles/', self.sync_from_roles, name='responsibility_sync_from_roles'),
        ]
        return custom_urls + urls

    def sync_from_roles(self, request):
        """
        Sync responsibility values from core.utils.roles
        """
        try:
            # Get all responsibility choices from roles.py
            choices = get_responsibility_choices()
            count = 0

            # Create Responsibility objects for each choice that doesn't exist
            for value, display_name in choices:
                if not Responsibility.objects.filter(name=display_name).exists():
                    Responsibility.objects.create(
                        name=display_name,
                        description=f'Auto-generated from roles system: {display_name}'
                    )
                    count += 1

            self.message_user(
                request,
                f'Successfully synced {count} new responsibilities from roles configuration.',
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f'Error syncing responsibilities: {str(e)}',
                messages.ERROR
            )

        return HttpResponseRedirect(reverse('admin:responsibility_responsibility_changelist'))
