from django.contrib import admin
from .models import ComplianceComment, NonConformanceComment

admin.site.register(ComplianceComment)
admin.site.register(NonConformanceComment)
