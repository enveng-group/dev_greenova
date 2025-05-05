import logging
from typing import Any, TypeVar, cast

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import DatabaseError, connection, models
from django.db.models import QuerySet
from django.utils import timezone

# Ensure consistent module naming by adjusting the import paths or PYTHONPATH setup.
# This will prevent the file from being detected under two different module names.


logger = logging.getLogger(__name__)
User = get_user_model()
UserType = TypeVar("UserType", bound=models.Model)  # Type variable for User model


class Company(models.Model):
    """Model representing a company or organization."""

    name: models.CharField = models.CharField(max_length=255, unique=True)
    logo: models.ImageField = models.ImageField(
        upload_to="company_logos/", blank=True, null=True
    )
    description: models.TextField = models.TextField(blank=True)
    website: models.URLField = models.URLField(blank=True)
    address: models.TextField = models.TextField(blank=True)
    phone: models.CharField = models.CharField(max_length=50, blank=True)
    email: models.EmailField = models.EmailField(blank=True)

    # Company type choices
    COMPANY_TYPES = [
        ("client", "Client"),
        ("contractor", "Contractor"),
        ("consultant", "Consultant"),
        ("regulator", "Regulator"),
        ("internal", "Internal Department"),
        ("other", "Other"),
    ]
    company_type: models.CharField = models.CharField(
        max_length=20, choices=COMPANY_TYPES, default="client"
    )

    # Company size choices
    COMPANY_SIZES = [
        ("small", "Small (1-49 employees)"),
        ("medium", "Medium (50-249 employees)"),
        ("large", "Large (250+ employees)"),
    ]
    size: models.CharField = models.CharField(
        max_length=10, choices=COMPANY_SIZES, blank=True
    )

    # Industry sector choices
    INDUSTRY_SECTORS = [
        ("manufacturing", "Manufacturing"),
        ("construction", "Construction"),
        ("mining", "Mining"),
        ("energy", "Energy"),
        ("transportation", "Transportation"),
        ("government", "Government"),
        ("consulting", "Consulting"),
        ("other", "Other"),
    ]
    industry: models.CharField = models.CharField(
        max_length=20, choices=INDUSTRY_SECTORS, blank=True
    )

    # Company status
    is_active: models.BooleanField = models.BooleanField(default=True)

    # Many-to-many relationship with users
    members: models.Manager[User] = models.ManyToManyField(
        User, through="CompanyMembership", related_name="companies"
    )

    # For typing purposes - the projects field is a reverse relation added by Django
    projects: models.QuerySet

    # Timestamps
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_default_company() -> int:
        """
        Return the ID of the default 'TBA' company.
        Used as default for foreign keys to ensure data integrity.
        """
        return 1

    class Meta:
        app_label = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name) if self.name else "Unnamed Company"

    def get_member_count(self) -> int:
        """Get count of company members."""
        return self.members.all().count()

    def get_active_projects_count(self) -> int:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM pragma_table_info('projects_project')
                    WHERE name = 'is_active'
                    """
                )
                is_active_exists = cursor.fetchone()[0] > 0
            if is_active_exists:
                return self.projects.filter(is_active=True).count()
            return self.projects.count()
        except DatabaseError as exc:
            logger.error("Error counting active projects: %s", str(exc))
            return 0

    def get_members_by_role(self, role: str) -> QuerySet[UserType]:
        """Get all users with the specified role in this company."""
        return cast(
            QuerySet[UserType],
            User.objects.filter(
                companymembership__company=self, companymembership__role=role
            ),
        )

    def add_member(self, user: UserType, role: str = "member") -> None:
        """Add a user to the company with the specified role."""
        if not CompanyMembership.objects.filter(company=self, user=user).exists():
            CompanyMembership.objects.create(company=self, user=user, role=role)
            username = getattr(user, "username", "Unknown user")
            logger.info(
                "Added user %s to company %s with role %s", username, self.name, role
            )

    def remove_member(self, user: UserType) -> None:
        """Remove a user from the company."""
        CompanyMembership.objects.filter(company=self, user=user).delete()
        username = getattr(user, "username", "Unknown user")
        logger.info("Removed user %s from company %s", username, self.name)


class CompanyMembership(models.Model):
    """Through model for company memberships."""

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("member", "Member"),
        ("client_contact", "Client Contact"),
        ("contractor", "Contractor"),
        ("view_only", "View Only"),
    ]

    company: models.ForeignKey = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="memberships"
    )
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_memberships"
    )
    role: models.CharField = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="member"
    )
    department: models.CharField = models.CharField(max_length=100, blank=True)
    position: models.CharField = models.CharField(max_length=100, blank=True)
    date_joined: models.DateTimeField = models.DateTimeField(default=timezone.now)
    is_primary: models.BooleanField = models.BooleanField(
        default=False, help_text="Designates if this is the user's primary company."
    )

    class Meta:
        unique_together = ["user", "company"]
        ordering = ["company", "user"]
        verbose_name = "Company Membership"
        verbose_name_plural = "Company Memberships"

    def __str__(self) -> str:
        """String representation with proper type checking."""
        username = (
            getattr(self.user, "username", "Unknown user")
            if self.user
            else "Unknown user"
        )
        company_name = (
            getattr(self.company, "name", "Unknown company")
            if self.company
            else "Unknown company"
        )
        return f"{username} - {company_name} ({self.role})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to ensure only one company is primary."""
        if self.is_primary:
            # Set all other memberships for this user as not primary
            CompanyMembership.objects.filter(user=self.user, is_primary=True).exclude(
                pk=self.pk if self.pk else 0
            ).update(is_primary=False)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        """Validate that a company can only have one owner."""
        if self.role == "owner":
            existing_owner = (
                CompanyMembership.objects.filter(company=self.company, role="owner")
                .exclude(pk=self.pk if self.pk else 0)
                .exists()
            )

            if existing_owner:
                raise ValidationError({"role": "A company can only have one owner."})


class CompanyDocument(models.Model):
    """Model for storing company documents."""

    company: models.ForeignKey = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="documents"
    )
    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True)
    file: models.FileField = models.FileField(upload_to="company_documents/")
    document_type: models.CharField = models.CharField(max_length=100, blank=True)
    uploaded_by: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_company_documents",
    )
    uploaded_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Company Document"
        verbose_name_plural = "Company Documents"

    def __str__(self) -> str:
        """String representation with proper type checking."""
        doc_name = self.name if self.name else "Unnamed Document"
        company_name = (
            getattr(self.company, "name", "Unknown company")
            if self.company
            else "Unknown company"
        )
        return f"{doc_name} ({company_name})"
