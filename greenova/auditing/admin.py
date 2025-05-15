from django.contrib import admin, messages
from .models import ComplianceComment, NonConformanceComment, Audit, AuditEntry, Mitigation, CorrectiveAction

admin.site.register(ComplianceComment)
admin.site.register(NonConformanceComment)

class CorrectiveActionInline(admin.TabularInline):
    model = CorrectiveAction
    extra = 1


class MitigationInline(admin.TabularInline):
    model = Mitigation
    extra = 1
    def get_formset(self, request, obj=None, **kwargs):
        if obj and obj.finding != "noncompliant":
            messages.warning(request, "Mitigations should only be added to non-compliant entries.")
        return super().get_formset(request, obj, **kwargs)

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "entry_count")
    readonly_fields = ("entry_count",)
    filter_horizontal = ("mechanisms",)

    def entry_count(self, obj):
        return obj.entries.count()
    entry_count.short_description = "Audit Entry Count"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        obj = form.instance
        # clear existing entries
        AuditEntry.objects.filter(audit=obj).delete()

        obj.generate_entries_from_mechanisms()

        if obj.entries.count() == 0:
            self.message_user(
                request,
                "No obligations matched the selected mechanisms. No audit entries were created.",
                level=messages.WARNING
            )
        else:
            self.message_user(
                request,
                f"{obj.entries.count()} audit entries successfully created.",
                level=messages.SUCCESS
            )

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "audit", "obligation", "status", "finding")
    list_filter = ("finding",)
    inlines = [MitigationInline]

@admin.register(Mitigation)
class MitigationAdmin(admin.ModelAdmin):
    list_display = ("id", "audit_entry", "status", "created_at")
    inlines = [CorrectiveActionInline]


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    list_display = ("id", "mitigation", "status", "assigned_to", "due_date")
