from _typeshed import Incomplete
from django.contrib.auth.models import AbstractUser
from django.db import models

logger: Incomplete

class EnvironmentalObligation(models.Model):
    name: Incomplete
    description: Incomplete
    due_date: Incomplete
    is_complete: Incomplete
    created_at: Incomplete
    updated_at: Incomplete

class CustomUser(AbstractUser):
    email: Incomplete
    is_mfa_enabled: Incomplete
    company: Incomplete

class UserProfile(models.Model):
    user: Incomplete
    display_name: Incomplete
    preferences: Incomplete
    avatar: Incomplete
    updated_at: Incomplete

class AuditLog(models.Model):
    user: Incomplete
    action: Incomplete
    object_type: Incomplete
    object_id: Incomplete
    message: Incomplete
    timestamp: Incomplete
    ip_address: Incomplete
    extra_data: Incomplete

    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
