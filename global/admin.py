from django.contrib import admin
from .models import Obligation
from responsibility.models import Responsibility

admin.site.register(Obligation)
admin.site.register(Responsibility)
