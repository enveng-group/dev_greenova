from django.contrib import admin

from .models import BugReport


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    """Admin configuration for BugReport model."""

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
