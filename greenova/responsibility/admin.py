from django.contrib import admin
from .models import ResponsibilityRole, ResponsibilityAssignment


@admin.register(ResponsibilityRole)
class ResponsibilityRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'company_role', 'is_active')
    list_filter = ('company', 'is_active', 'company_role')
    search_fields = ('name', 'description', 'company__name')
    fieldsets = (
        (None, {
            'fields': ('name', 'company', 'description')
        }),
        ('Role Configuration', {
            'fields': ('company_role', 'is_active')
        }),
    )


@admin.register(ResponsibilityAssignment)
class ResponsibilityAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'obligation', 'role', 'created_by', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'obligation__obligation_number')
    raw_id_fields = ('user', 'obligation', 'role', 'created_by')
