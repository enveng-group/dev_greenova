from django.contrib import admin

from .models import Company, CompanyDocument, CompanyMembership


class CompanyMembershipInline(admin.TabularInline):
    model = CompanyMembership
    extra = 1
    raw_id_fields = ('user',)

class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    extra = 1
    raw_id_fields = ('uploaded_by',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'industry', 'is_active', 'get_member_count')
    list_filter = ('company_type', 'industry', 'is_active')
    search_fields = ('name', 'description', 'website')
    inlines = (CompanyMembershipInline, CompanyDocumentInline)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'address', 'phone', 'email')
        }),
        ('Classification', {
            'fields': ('company_type', 'size', 'industry', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'department', 'position', 'is_primary')
    list_filter = ('role', 'is_primary')
    search_fields = ('user__username', 'company__name', 'department', 'position')
    raw_id_fields = ('user', 'company')


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('name', 'description', 'company__name')
    raw_id_fields = ('company', 'uploaded_by')
