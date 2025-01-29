from django.contrib import admin
from .models import Obligation

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    list_display = ('obligation_number', 'project_name', 'status', 'action_due_date', 'responsibility')
    list_filter = ('project_name', 'status', 'action_due_date')
    search_fields = ('obligation_number', 'obligation', 'project_name')
    date_hierarchy = 'action_due_date'