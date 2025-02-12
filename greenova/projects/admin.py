from django.contrib import admin
from .models import Project, Obligation

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    list_display = ('obligation_number', 'project', 'status', 'primary_environmental_mechanism')
    list_filter = ('status', 'project', 'primary_environmental_mechanism')
    search_fields = (
        'obligation_number', 
        'obligation', 
        'environmental_aspect',
        'accountability',
        'responsibility'
    )