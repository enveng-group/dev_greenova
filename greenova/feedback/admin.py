from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import BugReport


class BugReportAdminForm(forms.ModelForm):
    """Admin form for BugReport with helpful field descriptions."""

    class Meta:
        model = BugReport
        fields = '__all__'


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    """Admin configuration for BugReport model."""

    form = BugReportAdminForm

    list_display = ('title', 'created_by', 'created_at', 'status', 'severity', 'frequency', 'impact_severity')
    list_filter = ('status', 'severity', 'frequency', 'impact_severity', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    fieldsets = (
        ('Summary', {
            'fields': ('title', 'description')
        }),
        ('Environment', {
            'fields': ('application_version', 'operating_system', 'browser', 'device_type')
        }),
        ('Problem Details', {
            'fields': ('steps_to_reproduce', 'expected_behavior', 'actual_behavior')
        }),
        ('Technical Information', {
            'fields': ('error_messages', 'trace_report')
        }),
        ('Impact Assessment', {
            'fields': ('frequency', 'impact_severity', 'user_impact')
        }),
        ('Additional Information', {
            'fields': ('workarounds', 'additional_comments')
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
        ('Admin Actions', {
            'fields': ('github_issue_url', 'severity', 'status', 'admin_comment')
        }),
    )

    actions = ['mark_as_rejected', 'mark_as_in_progress', 'mark_as_resolved', 'mark_as_closed']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        self._add_help_text_to_fields(form)
        return form

    def _add_help_text_to_fields(self, form):
        """Add helper text to form fields."""
        field_help = {
            'title': _("A brief, descriptive title of the issue. Example: 'Dashboard fails to load environmental metrics when filtering by project'"),
            'description': _('A concise summary of the problem. Focus on what happened, when it happened, and the context.'),
            'application_version': _("The version of Greenova where the bug was encountered. Check the footer of any Greenova page or look at the 'About' section in settings."),
            'operating_system': _('Your operating system and version (e.g., Windows 10, macOS 11.2, Ubuntu 20.04).'),
            'browser': _('Browser name and version (e.g., Chrome 89.0, Firefox 86.0). Leave blank if not applicable.'),
            'device_type': _('Type of device (e.g., desktop, laptop, smartphone). Include device model if on mobile.'),
            'steps_to_reproduce': _('Detailed numbered steps to reproduce the issue. Start from a known state and be specific about what you clicked, typed, or selected.'),
            'expected_behavior': _('What you expected to happen when following the steps above.'),
            'actual_behavior': _('What actually happened instead. Be specific about error messages, unexpected behavior, or missing functionality.'),
            'error_messages': _('Copy and paste the exact error text rather than paraphrasing. Include any error codes or numbers.'),
            'trace_report': _("If available, include the Django traceback or browser console logs. For Django errors: look for the section labeled 'Traceback', click on 'Switch to copy-and-paste view', and copy the entire trace report."),
            'frequency': _('How often the issue occurs. Select the option that best matches your experience.'),
            'impact_severity': _('How severe the issue is: Minor (causes inconvenience), Major (prevents completing specific tasks), Critical (prevents core functionality, data loss, security risks).'),
            'user_impact': _('How the issue affects user experience. Mention any deadlines or business processes affected.'),
            'workarounds': _("Any temporary solutions you've found to work around the issue."),
            'additional_comments': _("Any other relevant information, patterns you've noticed, or when the issue started occurring."),
            'github_issue_url': _("URL to the associated GitHub issue if one has been created."),
            'severity': _("Administrator's assessment of bug severity."),
            'status': _("Current status of the bug report."),
            'admin_comment': _("Internal notes about this bug report (not visible to users)."),
        }

        for field_name, help_text in field_help.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].help_text = help_text

    @admin.action(
        description='Mark selected reports as rejected'
    )
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')

    @admin.action(
        description='Mark selected reports as in progress'
    )
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(
        description='Mark selected reports as resolved'
    )
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')

    @admin.action(
        description='Mark selected reports as closed'
    )
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
