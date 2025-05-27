"""
Models for company and organization data in Greenova.

This module defines Django ORM models for companies, memberships, documents,
and obligations in the Greenova application.
"""

import logging
from typing import TYPE_CHECKING, Any, ClassVar, cast

from beartype import beartype
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connection, models
from django.utils import timezone

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser as UserType
else:
    UserType = Any


class Company(models.Model):
    """Model representing a company or organization."""

    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=255, unique=True)  # Company name must be unique
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)
    users: models.ManyToManyField[Any, Any] = models.ManyToManyField(
        get_user_model(), related_name="companies"
    )

    # Company type choices
    COMPANY_TYPES: ClassVar[list[tuple[str, str]]] = [
        ("client", "Client"),
        ("contractor", "Contractor"),
        ("consultant", "Consultant"),
        ("regulator", "Regulator"),
        ("internal", "Internal Department"),
        ("other", "Other"),
    ]
    company_type = models.CharField(
        max_length=20, choices=COMPANY_TYPES, default="client"
    )

    # Company size choices
    COMPANY_SIZES: ClassVar[list[tuple[str, str]]] = [
        ("small", "Small (1-49 employees)"),
        ("medium", "Medium (50-249 employees)"),
        ("large", "Large (250+ employees)"),
    ]
    size = models.CharField(max_length=10, choices=COMPANY_SIZES, blank=True)

    # Industry sector choices
    INDUSTRY_SECTORS: ClassVar[list[tuple[str, str]]] = [
        ("manufacturing", "Manufacturing"),
        ("construction", "Construction"),
        ("mining", "Mining"),
        ("energy", "Energy"),
        ("transportation", "Transportation"),
        ("government", "Government"),
        ("consulting", "Consulting"),
        ("other", "Other"),
    ]
    industry = models.CharField(max_length=20, choices=INDUSTRY_SECTORS, blank=True)

    # Company status
    is_active = models.BooleanField(default=True)

    @staticmethod
    @beartype
    def get_default_company() -> int:
        """Return the ID of the default 'TBA' company.

        Returns:
            The ID of the default company (int).
        """
        return 1

    class Meta:
        """Meta options for the Company model."""

        verbose_name: ClassVar[str] = "Company"
        verbose_name_plural: ClassVar[str] = "Companies"
        ordering: ClassVar[list[str]] = ["name"]

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the company."""
        return self.name

    @beartype
    def get_member_count(self) -> int:
        """Get count of company members.

        Returns:
            The number of users associated with this company.
        """
        return int(self.users.count())

    @beartype
    def get_active_projects_count(self) -> int:
        """Get count of active projects associated with this company.

        Returns:
            The number of active projects associated with this company.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM pragma_table_info('projects_project')
                    WHERE name = 'is_active'
                    """
                )
                result = cursor.fetchone()
                is_active_exists = result[0] > 0 if result else False
            if is_active_exists and hasattr(self, "projects"):
                return int(
                    self.projects.filter(is_active=True).count()
                )
            elif hasattr(self, "projects"):
                return int(
                    self.projects.count()
                )
            return 0
        except Exception as e:
            logger.error("Error counting active projects: %s", str(e))
            return 0

    @beartype
    def get_members_by_role(self, role: str) -> models.QuerySet[Any]:
        """Get all users with the specified role in this company.

        Args:
            role: The role to filter users by.

        Returns:
            QuerySet of users with the specified role in this company.
        """
        return cast(
            models.QuerySet[Any],
            get_user_model().objects.filter(  # type: ignore[attr-defined]
                companymembership__company=self,
                companymembership__role=role,
            ),
        )

    @beartype
    def add_member(self, user: 'UserType', role: str = "member") -> None:
        """Add a user to the company with the specified role.

        Args:
            user: The user to add.
            role: The role to assign to the user (default: "member").
        """
        company_membership_model = apps.get_model('company', 'CompanyMembership')
        if not company_membership_model.objects.filter(
            company=self, user=user
        ).exists():
            company_membership_model.objects.create(
                company=self, user=user, role=role
            )
            logger.info(
                "Added user %s to company %s with role %s",
                getattr(user, "username", str(user)),
                self.name,
                role,
            )

    @beartype
    def remove_member(self, user: 'UserType') -> None:
        """Remove a user from the company.

        Args:
            user: The user to remove.
        """
        company_membership_model = apps.get_model('company', 'CompanyMembership')
        company_membership_model.objects.filter(
            company=self, user=user
        ).delete()
        logger.info(
            "Removed user %s from company %s",
            getattr(user, "username", str(user)),
            self.name,
        )

    @beartype
    def clean(self) -> None:
        """Ensure data integrity for Company-User relationship.

        Raises:
            ValidationError: If a company has no users.
        """
        if self.pk and self.users.count() == 0:
            raise ValidationError("A company must have at least one user.")


class CompanyMembership(models.Model):
    """Model representing a user's membership in a company."""

    ROLE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("member", "Member"),
        ("client_contact", "Client Contact"),
        ("contractor", "Contractor"),
        ("view_only", "View Only"),
    ]

    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="company_memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_primary = models.BooleanField(
        default=False,
        help_text="Designates if this is the user's primary company."
    )

    class Meta:
        """Meta options for the CompanyMembership model."""

        unique_together: ClassVar[list[str]] = ["user", "company"]
        ordering: ClassVar[list[str]] = ["company", "user"]
        verbose_name: ClassVar[str] = "Company Membership"
        verbose_name_plural: ClassVar[str] = "Company Memberships"

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the company membership.

        Returns:
            String representation of the membership.
        """
        return (
            f"{getattr(self.user, 'username', str(self.user))} - "
            f"{self.company.name} ({self.role})"
        )

    @beartype
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to ensure only one company is primary.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        if self.is_primary:
            (self.__class__.objects  # type: ignore[attr-defined]
                .filter(user=self.user, is_primary=True)
                .exclude(id=getattr(self, 'id', 0))
                .update(is_primary=False)
             )
        super().save(*args, **kwargs)

    @beartype
    def clean(self) -> None:
        """Validate that a company can only have one owner.

        Raises:
            ValidationError: If a company already has an owner.
        """
        if self.role == "owner":
            existing_owner = (
                self.__class__.objects  # type: ignore[attr-defined]
                .filter(company=self.company, role="owner")
                .exclude(id=getattr(self, 'id', 0))
                .exists()
            )
            if existing_owner:
                raise ValidationError({"role": "A company can only have one owner."})


class CompanyDocument(models.Model):
    """Model for storing company documents."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="company_documents/")
    document_type = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_company_documents",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the CompanyDocument model."""

        ordering: ClassVar[list[str]] = ["-uploaded_at"]
        verbose_name: ClassVar[str] = "Company Document"
        verbose_name_plural: ClassVar[str] = "Company Documents"

    def __str__(self) -> str:
        """Return a string representation of the company document."""
        return f"{self.name} ({self.company.name})"


class Obligation(models.Model):
    """Model representing an environmental obligation."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="obligations",
        help_text="The company associated with this obligation.",
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("not_started", "Not Started"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        default="not_started",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Obligation model."""

        ordering: ClassVar[list[str]] = ["due_date"]
        verbose_name: ClassVar[str] = "Obligation"
        verbose_name_plural: ClassVar[str] = "Obligations"

    def __str__(self) -> str:
        """Return a string representation of the obligation."""
        return self.name
