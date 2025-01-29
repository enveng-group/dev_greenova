from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "ip_address")
    list_filter = ("action", "timestamp")
    search_fields = ("user__username", "ip_address", "details")
    readonly_fields = ("timestamp", "ip_address")
