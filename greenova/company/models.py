# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Company models for the company app.

This module provides the Company, CompanyMembership, and CompanyDocument models,
with strict type annotations, runtime type checking, and Protocol Buffer integration.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protobuf3 integration for company models
    - Lifecycle hooks for membership management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from .constants import (
    COMPANY_TYPE_CHOICES,
    COMPANY_TYPE_PRIVATE,
)
from .validators import validate_company_name

logger = logging.getLogger(__name__)

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = object  # fallback for type checking

try:
    from greenova.protobuf.company_pb2 import (
        CompanyDocumentProto,
        CompanyMembershipProto,
        CompanyProto,
    )
except ImportError:
    CompanyProto = None
    CompanyMembershipProto = None
    CompanyDocumentProto = None


class Company(ProtoBufMixin, models.Model):  # type: ignore[misc]
    """Model representing a company or organization."""

    pb_model = CompanyProto

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validate_company_name],
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    company_type = models.CharField(
        max_length=20,
        choices=COMPANY_TYPE_CHOICES,
        default=COMPANY_TYPE_PRIVATE,
    )

    COMPANY_SIZES = [
        ("small", "Small (1-49 employees)"),
        ("medium", "Medium (50-249 employees)"),
        ("large", "Large (250+ employees)"),
    ]
    size = models.CharField(
        max_length=10,
        choices=COMPANY_SIZES,
        blank=True,
    )

    COMPANY_TYPES = (
        ("private", "Private"),
        ("public", "Public"),
        ("government", "Government"),
        ("nonprofit", "Non-profit"),
    )
    INDUSTRY_SECTORS = (
        ("energy", "Energy"),
        ("manufacturing", "Manufacturing"),
        ("agriculture", "Agriculture"),
        ("services", "Services"),
        ("construction", "Construction"),
        ("other", "Other"),
    )
    industry = models.CharField(
        max_length=20,
        choices=INDUSTRY_SECTORS,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    members = models.ManyToManyField(
        User,
        through="CompanyMembership",
        related_name="companies",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    @beartype
    def get_default_company() -> int:
        """Return the ID of the default 'TBA' company.

        Used as default for foreign keys to ensure data integrity.

        Returns:
            int: The ID of the default company.

        """
        return 1

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]
        permissions = [
            ("manage_members", "Can manage company members"),
        ]
        default_permissions = ("add", "change", "delete", "view")

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the company.

        Returns:
            str: The name of the company.

        """
        return self.name

    # Slug is now set via pre_save signal in signals.py

    @beartype
    def get_member_count(self) -> int:
        """Get count of company members.

        Returns:
            int: The number of members in the company.

        """
        return self.members.count()

    @beartype
    def get_active_projects_count(self) -> int:
        """Get count of active projects associated with this company.

        Returns:
            int: The number of active projects.

        """
        from django.db import connection

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM pragma_table_info('projects_project')
                    WHERE name = 'is_active'
                    """,
                )
                is_active_exists = cursor.fetchone()[0] > 0

            if is_active_exists:
                return self.projects.filter(is_active=True).count()
            return self.projects.count()
        except Exception as e:
            logger.exception("Error counting active projects: %s", str(e))
            return 0

    @beartype
    def get_members_by_role(self, role: str) -> QuerySet:
        """Get all users with the specified role in this company.

        Args:
            role: The role to filter members by.

        Returns:
            QuerySet: A queryset of users with the specified role.

        """
        return User.objects.filter(
            companymembership__company=self,
            companymembership__role=role,
        )

    @beartype
    def add_member(self, user: User, role: str = "member") -> None:
        """Add a user to the company with the specified role.

        Args:
            user: The user to add.
            role: The role to assign to the user.

        """
        if not CompanyMembership.objects.filter(company=self, user=user).exists():
            CompanyMembership.objects.create(
                company=self,
                user=user,
                role=role,
            )
            logger.info(
                "Added user %s to company %s with role %s",
                user.username,
                self.name,
                role,
            )

    @beartype
    def remove_member(self, user: User) -> None:
        """Remove a user from the company.

        Args:
            user: The user to remove.

        """
        CompanyMembership.objects.filter(company=self, user=user).delete()
        logger.info("Removed user %s from company %s", user.username, self.name)


class CompanyMembership(ProtoBufMixin, models.Model):  # type: ignore[misc]
    """Through model for company memberships."""

    pb_model = CompanyMembershipProto

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("member", "Member"),
        ("client_contact", "Client Contact"),
        ("contractor", "Contractor"),
        ("view_only", "View Only"),
    ]

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="company_memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="member",
    )
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_primary = models.BooleanField(
        default=False,
        help_text="Designates if this is the user's primary company.",
    )

    class Meta:
        unique_together = ["user", "company"]
        ordering = ["company", "user"]
        verbose_name = "Company Membership"
        verbose_name_plural = "Company Memberships"

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the company membership.

        Returns:
            str: The user-company-role string.

        """
        return f"{self.user.username} - {self.company.name} ({self.role})"

    # Single primary logic is now handled via pre_save signal in signals.py

    @beartype
    def clean(self) -> None:
        """Validate that a company can only have one owner.

        Raises:
            ValidationError: If a company already has an owner.

        """
        if self.role == "owner":
            existing_owner = (
                CompanyMembership.objects.filter(
                    company=self.company,
                    role="owner",
                )
                .exclude(id=self.id or 0)
                .exists()
            )

            if existing_owner:
                raise ValidationError({"role": "A company can only have one owner."})


class CompanyDocument(ProtoBufMixin, models.Model):
    """Model for storing company documents.

    Attributes:
        company (ForeignKey): The company associated with the document.
        name (str): The name of the document.
        description (str): A brief description of the document.
        file (FileField): The file associated with the document.
        document_type (str): The type of document.
        uploaded_by (ForeignKey): The user who uploaded the document.
        uploaded_at (DateTimeField): The timestamp when the document was uploaded.

    """

    pb_model = CompanyDocumentProto

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="company_documents/")
    document_type = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_company_documents",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Company Document"
        verbose_name_plural = "Company Documents"

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the document.

        Returns:
            str: The name of the document and the associated company.

        """
        return f"{self.name} ({self.company.name})"
