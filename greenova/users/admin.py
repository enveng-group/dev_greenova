from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'department', 'created_at')
    search_fields = ('user__username', 'job_title', 'department')
    list_filter = ('department', 'created_at')