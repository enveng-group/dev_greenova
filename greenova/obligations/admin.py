from django.contrib import admin

from .models import Obligation


@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    list_display = (
        'obligation_number',
        'project_name',
        'status',
        'action_due_date',
        'responsibility',
        'is_overdue',
    )
    list_filter = (
        'project_name',
        'status',
        'recurring_obligation',
        'inspection',
        'site_or_desktop',
    )
    search_fields = (
        'obligation_number',
        'project_name',
        'obligation',
        'responsibility',
        'person_email',
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    fieldsets = (
        (
            'Primary Information',
            {
                'fields': (
                    'obligation_number',
                    'project_name',
                    'primary_environmental_mechanism',
                    'procedure',
                    'environmental_aspect',
                    'obligation',
                )
            },
        ),
        (
            'Responsibility',
            {
                'fields': (
                    'accountability',
                    'responsibility',
                    'project_phase',
                    'person_email',
                )
            },
        ),
        (
            'Dates and Status',
            {'fields': ('action_due_date', 'close_out_date', 'status')},
        ),
        (
            'Comments and Evidence',
            {
                'fields': (
                    'supporting_information',
                    'general_comments',
                    'compliance_comments',
                    'non_conformance_comments',
                    'evidence',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Recurring Information',
            {
                'fields': (
                    'recurring_obligation',
                    'recurring_frequency',
                    'recurring_status',
                    'recurring_forcasted_date',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Inspection Details',
            {
                'fields': (
                    'inspection',
                    'inspection_frequency',
                    'site_or_desktop',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Additional Information',
            {
                'fields': (
                    'new_control_action_required',
                    'obligation_type',
                    'gap_analysis',
                    'notes_for_gap_analysis',
                    'covered_in_which_inspection_checklist',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Audit Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                    'created_by',
                    'updated_by',
                ),
                'classes': ('collapse',),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
